import shutil
import exiftool


# ── Tags que ExifTool puede ESCRIBIR ─────────────────────────────────────────
WRITABLE_TAGS = {
    "EXIF:Make",
    "EXIF:Model",
    "EXIF:Software",
    "EXIF:ModifyDate",
    "EXIF:ISO",
    "EXIF:FNumber",
    "EXIF:ExposureTime",
    "EXIF:FocalLength",
    "XMP:CreatorTool",
    "XMP:CreateDate",
    "EXIF:GPSLatitude",
    "EXIF:GPSLongitude",
}

# ── Tags de solo lectura ──────────────────────────────────────────────────────
READONLY_TAGS = {
    "File:FileName",
    "File:FileSize",
    "File:FileType",
    "File:MIMEType",
    "File:ImageWidth",
    "File:ImageHeight",
    "Composite:Megapixels",
}

# ── Mapa raw_tag → label legible ──────────────────────────────────────────────
IMPORTANT_TAGS: dict[str, str] = {
    "File:FileName":        "File Name",
    "File:FileSize":        "File Size",
    "File:FileType":        "File Type",
    "File:MIMEType":        "MIME Type",
    "File:ImageWidth":      "Width",
    "File:ImageHeight":     "Height",
    "Composite:Megapixels": "Megapixels",
    "EXIF:Make":            "Camera Brand",
    "EXIF:Model":           "Camera Model",
    "EXIF:Software":        "Software",
    "EXIF:ModifyDate":      "Last Modified",
    "EXIF:ISO":             "ISO",
    "EXIF:FNumber":         "Aperture",
    "EXIF:ExposureTime":    "Shutter Speed",
    "EXIF:FocalLength":     "Focal Length",
    "XMP:CreatorTool":      "Editing Software",
    "XMP:CreateDate":       "Creation Date",
}


def extract_metadata(file_path: str) -> list[dict]:
    """
    Extrae metadatos de un archivo con ExifTool.
    Devuelve una lista de dicts con tag, raw_tag, value, editable.
    """
    with exiftool.ExifToolHelper() as et:
        raw = et.get_metadata(file_path)[0]

    table = []

    for raw_tag, label in IMPORTANT_TAGS.items():
        value = raw.get(raw_tag)
        if value is not None:
            table.append({
                "tag":      label,
                "raw_tag":  raw_tag,
                "value":    str(value),
                "editable": raw_tag in WRITABLE_TAGS,
            })

    # GPS — tratamiento especial por los refs de hemisferio
    lat    = raw.get("EXIF:GPSLatitude")
    lon    = raw.get("EXIF:GPSLongitude")
    latref = raw.get("EXIF:GPSLatitudeRef")
    lonref = raw.get("EXIF:GPSLongitudeRef")

    if lat and lon and latref and lonref:
        lat_signed = -lat if latref == "S" else lat
        lon_signed = -lon if lonref == "W" else lon

        table.append({
            "tag":      "GPS Latitude",
            "raw_tag":  "EXIF:GPSLatitude",
            "value":    str(lat_signed),
            "editable": True,
        })
        table.append({
            "tag":      "GPS Longitude",
            "raw_tag":  "EXIF:GPSLongitude",
            "value":    str(lon_signed),
            "editable": True,
        })
        table.append({
            "tag":      "Google Maps Location",
            "raw_tag":  "Composite:GPSPosition",
            "value":    f"https://maps.google.com/?q={lat_signed},{lon_signed}",
            "editable": False,
        })

    return table


def write_metadata(src_path: str, metadata_items: list[dict], dest_path: str) -> str:
    """
    Copia src_path → dest_path y escribe los metadatos editables con ExifTool.
    Devuelve dest_path.
    """
    shutil.copy2(src_path, dest_path)

    tags_to_write = {
        item["raw_tag"]: item["value"]
        for item in metadata_items
        if item.get("editable", False)
    }

    if not tags_to_write:
        return dest_path

    with exiftool.ExifToolHelper() as et:
        et.set_tags(
            [dest_path],
            tags=tags_to_write,
            params=["-overwrite_original"],  # evita generar archivos _original
        )

    return dest_path