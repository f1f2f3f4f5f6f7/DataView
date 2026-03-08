import os
import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.models.metadata_model import MetadataTable
from app.services.exif_service import extract_metadata
from app.services.file_service import (
    export_csv,
    export_pdf,
    export_jpg,
    export_image_with_metadata,
)
from app.utils.temp_manager import (
    save_upload_to_temp,
    make_temp_dir,
    cleanup_file,
    cleanup_dir,
)

router = APIRouter(prefix="/api", tags=["metadata"])


# ── 1. Subir archivo → extraer metadatos ─────────────────────────────────────

@router.post("/upload", response_model=MetadataTable)
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1] or ".tmp"
    contents = await file.read()
    tmp_path = save_upload_to_temp(contents, suffix=ext)

    try:
        metadata = extract_metadata(tmp_path)
    finally:
        cleanup_file(tmp_path)

    return {"metadata": metadata}


# ── 2. Exports de la tabla de metadatos (CSV / PDF / JPG visual) ─────────────

@router.post("/export/csv")
def export_csv_endpoint(data: MetadataTable):
    """Exporta la tabla de metadatos como archivo CSV."""
    tmp_path = save_upload_to_temp(b"", suffix=".csv")
    export_csv([item.dict() for item in data.metadata], tmp_path)
    return FileResponse(tmp_path, filename="metadata.csv", media_type="text/csv")


@router.post("/export/pdf")
def export_pdf_endpoint(data: MetadataTable):
    """Exporta la tabla de metadatos como PDF."""
    tmp_path = save_upload_to_temp(b"", suffix=".pdf")
    export_pdf([item.dict() for item in data.metadata], tmp_path)
    return FileResponse(tmp_path, filename="metadata.pdf", media_type="application/pdf")


@router.post("/export/jpg")
def export_jpg_endpoint(data: MetadataTable):
    """Exporta la tabla de metadatos como imagen JPG visual (no la imagen original)."""
    tmp_path = save_upload_to_temp(b"", suffix=".jpg")
    export_jpg([item.dict() for item in data.metadata], tmp_path)
    return FileResponse(tmp_path, filename="metadata.jpg", media_type="image/jpeg")


# ── 3. Export principal: imagen original con metadatos editados escritos ──────

@router.post("/export/image")
async def export_image_endpoint(
    file: UploadFile = File(...),
    metadata: str = Form(...),
):
    """
    Recibe la imagen original + los metadatos editados por el usuario.
    Escribe los cambios con ExifTool y devuelve la imagen con los metadatos nuevos.
    Este es el export principal del flujo de edición.
    """
    try:
        metadata_items = json.loads(metadata)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El campo 'metadata' no es JSON válido.")

    ext      = os.path.splitext(file.filename or "")[1] or ".jpg"
    tmp_dir  = make_temp_dir()
    src_path  = os.path.join(tmp_dir, f"input{ext}")
    dest_path = os.path.join(tmp_dir, f"output{ext}")

    try:
        contents = await file.read()
        with open(src_path, "wb") as f:
            f.write(contents)

        export_image_with_metadata(src_path, metadata_items, dest_path)

        return FileResponse(
            dest_path,
            media_type=file.content_type or "application/octet-stream",
            filename=f"edited_{file.filename}",
        )
    except Exception as e:
        cleanup_dir(tmp_dir)
        raise HTTPException(status_code=500, detail=str(e))