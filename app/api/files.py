from fastapi import APIRouter, HTTPException, Query

from app.services.file_service import scan_directory
from app.schemas.file import DirectoryScanResponse
from typing import Literal

router = APIRouter(prefix="/files", tags=["files"])

@router.get("", response_model=DirectoryScanResponse)
def list_files(path: str = Query(..., description="Directory path to scan"),
               sort_by: Literal["name", "size", "last_modified"] | None = Query(None, description="Field to sort by"),
               order: Literal["asc", "desc"] | None = Query("asc", description="Sort Order")
               ):
    """Endpoint to list files in a given directory."""
    try:
        raw_files = scan_directory(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if sort_by:
        reverse = order == "desc" 
        # 'file' in lambda refers to each dictionary in the raw_files list 
        if sort_by == "name":
            raw_files.sort(key=lambda file: file["name"].lower(), reverse=reverse)

        elif sort_by == "size":
            raw_files.sort(key=lambda file: file["size_bytes"], reverse=reverse)

        elif sort_by == "last_modified":
            raw_files.sort(key=lambda file: file["last_modified"], reverse=reverse)    
    return {
        "path": path,
        "count": len(raw_files),
        "files": raw_files,
    }