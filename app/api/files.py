from fastapi import APIRouter, HTTPException, Query

from app.services.file_service import scan_directory
from app.schemas.file import FileInfo

router = APIRouter(prefix="/files", tags=["files"])

@router.get("", response_model=list[FileInfo])
def list_files(path: str = Query(..., description="Directory path to scan")):
    """Endpoint to list files in a given directory."""
    try:
        raw_files = scan_directory(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return raw_files