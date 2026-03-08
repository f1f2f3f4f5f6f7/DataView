from pydantic import BaseModel
from typing import List


class MetadataItem(BaseModel):
    tag: str        # Label legible: "Camera Brand"
    raw_tag: str    # Tag ExifTool original: "EXIF:Make"
    value: str
    editable: bool  # Si ExifTool puede escribir este tag


class MetadataTable(BaseModel):
    metadata: List[MetadataItem]