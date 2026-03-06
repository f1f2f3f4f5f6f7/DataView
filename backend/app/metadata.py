import exiftool
import os
from PIL import Image

def extract_metadata(file_path):

    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file_path)[0]

    table = []

    important_tags = {
        "File:FileName": "File Name",
        "File:FileSize": "File Size",
        "File:FileType": "File Type",
        "File:MIMEType": "MIME Type",

        "File:ImageWidth": "Width",
        "File:ImageHeight": "Height",
        "Composite:Megapixels": "Megapixels",

        "EXIF:Make": "Camera Brand",
        "EXIF:Model": "Camera Model",
        "EXIF:Software": "Software",
        "EXIF:ModifyDate": "Last Modified",

        "EXIF:ISO": "ISO",
        "EXIF:FNumber": "Aperture",
        "EXIF:ExposureTime": "Shutter Speed",
        "EXIF:FocalLength": "Focal Length",

        "XMP:CreatorTool": "Editing Software",
        "XMP:CreateDate": "Creation Date"
    }

    # Apilar los tags importantes  
    for key, label in important_tags.items():
        value = metadata.get(key)

        if value:
            table.append({
                "tag": label,
                "value": str(value)
            })

    # Agregar ubicación GPS
    lat = metadata.get("EXIF:GPSLatitude")
    lon = metadata.get("EXIF:GPSLongitude")
    latref = metadata.get("EXIF:GPSLatitudeRef")
    lonref = metadata.get("EXIF:GPSLongitudeRef")

    if lat and lon and latref and lonref:
        lat_signed = -lat if latref == "S" else lat
        lon_signed = -lon if lonref == "W" else lon


        table.append({
            "tag": "GPS Latitude",
            "value": str(lat_signed)
        })

        table.append({
            "tag": "GPS Longitude",
            "value": str(lon_signed)
        })

        maps_link = f"https://maps.google.com/?q={lat_signed},{lon_signed}"

        table.append({
            "tag": "Google Maps Location",
            "value": maps_link
        })

    return table
