from pydantic import BaseModel
from datetime import datetime


class FileInfo(BaseModel):
    name: str
    path: str
    extension: str | None
    size_bytes: int
    is_directory: bool
    last_modified: datetime

class DirectoryScanResponse(BaseModel):
    path: str
    count: int
    files: list[FileInfo]