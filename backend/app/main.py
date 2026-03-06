from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile

from .metadata import extract_metadata
from .export import export_csv, export_pdf, export_jpg
from .models import MetadataTable

app = FastAPI(
    title="Image Metadata API",
    description="Extract and export image metadata including GPS location.",
    version="1.0.0"
    )

@app.post("/api/upload", response_model=MetadataTable)
async def upload_file(file: UploadFile = File(...)):

    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=True) as tmp:

        tmp.write(contents)
        tmp.flush()

        metadata = extract_metadata(tmp.name)

    return {"metadata": metadata}

@app.post("/process", response_model=MetadataTable)
def process_metadata(data: MetadataTable):

    return {"metadata": data.metadata}


# ===============================
# Export CSV
# ===============================
@app.post("/export/csv")
def export_csv_file(data: MetadataTable):

    output = "metadata.csv"

    export_csv(
        [item.dict() for item in data.metadata],
        output
    )

    return FileResponse(output, filename="metadata.csv")

@app.post("/export/pdf")
def export_pdf_file(data: MetadataTable):

    output = "metadata.pdf"

    export_pdf(
        [item.dict() for item in data.metadata],
        output
    )

    return FileResponse(output, filename="metadata.pdf")


@app.post("/export/jpg")
def export_jpg_file(data: MetadataTable):

    output = "metadata.jpg"

    export_jpg(
        [item.dict() for item in data.metadata],
        output
    )

    return FileResponse(output, filename="metadata.jpg")
