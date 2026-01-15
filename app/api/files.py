from fastapi import APIRouter, HTTPException, Query

from app.services.file_service import scan_directory, plan_file_moves
from app.schemas.file import DirectoryScanResponse, PlannedMove, PlanResponse
from typing import Literal

router = APIRouter(prefix="/files", tags=["files"])

@router.get("", response_model=DirectoryScanResponse)
def list_files(path: str = Query(..., description="Directory path to scan"),
               
               #recursive scan option
               recursive: bool = Query(False, description="Enable heirarchial scan of subdirectories"),

               # Sorting parameters
               sort_by: Literal["name", "size", "last_modified"] | None = Query(None, description="Field to sort by"),
               order: Literal["asc", "desc"] = Query("asc", description="Sort Order"),
               

               #Filtering parameters
               ext: str | None = Query(None, description="Filter by file extension"),
               only: Literal["files", "dirs"] | None = Query(None, description="Filter by type"),
               min_size: int | None = Query(None, ge=0, description="Minimum file size in bytes"),
               max_size: int | None = Query(None, ge=0, description="Maximum file size in bytes")
               ):
    """Endpoint to list files in a given directory."""
    try:
        raw_files = scan_directory(path, recursive=recursive)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    # Filtering
    if ext: 
        raw_files = [f for f in raw_files if f["extension"] == ext]
    if only:
        raw_files = [f for f in raw_files if f["is_directory"] == (only == "dirs")]
    if min_size is not None:
       raw_files = [f for f in raw_files if f["size_bytes"] >= min_size]
    if max_size is not None:
       raw_files = [f for f in raw_files if f["size_bytes"] <= max_size]
    
    # Sorting
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

@router.get("/plan-moves", response_model=PlanResponse)
def plan_moves(path: str = Query(..., description="Directory path to organize")):
    """
    Endpoint to plan organization of files
    """

    try:
        plan = plan_file_moves(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "path": path,
        "count": len(plan),
        "moves": plan
    }
