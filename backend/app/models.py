from pydantic import BaseModel
from typing import List

class MetadataItem(BaseModel):
    tag: str
    value: str

class MetadataTable(BaseModel):
    metadata: List[MetadataItem]
