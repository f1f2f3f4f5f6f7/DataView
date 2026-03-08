from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.metadata_routes import router as metadata_router

app = FastAPI(
    title="DataView — Image Metadata API",
    description="Extrae, edita y reescribe metadatos de imágenes usando ExifTool.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metadata_router)