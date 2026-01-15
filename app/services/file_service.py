from pathlib import Path
from datetime import datetime
from app.core.config import SANDBOX_ROOT



EXTENSION_MAP = {
    ".pdf": "Documents",
    ".txt": "Documents",
    ".jpg": "Images",
    ".png": "Images",
    ".jpeg": "Images",
    ".zip": "Archives",
}

def check_path_validity(path: Path) -> bool:
    """
    Function to check if supplied path is valid 
    under predefined rules
    """
    if not path.is_relative_to(SANDBOX_ROOT):
        raise ValueError("Access to the specified path is not allowed")

    if not path.exists():
        raise ValueError("Path does not exist")
    
    if not path.is_dir():
        raise ValueError("Path is not a directory")
    
    return True

def plan_file_moves(path: str) -> list[dict]:
    """
    Dry-run planner: returns a list of planned file moves
    without modifying the filesystem
    """
    base_path = Path(path).resolve()

    check_path_validity(base_path)

    planned_moves: list[dict] = []

    for entry in base_path.iterdir():
        if entry.is_dir():
            continue  # Skip directories

        ext = entry.suffix.lower()
        target = EXTENSION_MAP.get(ext, "Others")

        destination_dir = base_path / target
        destination_path = destination_dir / entry.name

        if entry.parent == destination_dir:
            continue

        planned_moves.append({
            "source": str(entry.resolve()),
            "destination": str(destination_path.resolve()),
            "reason": "Classification based on extension"
        })
    
    return planned_moves

def scan_directory(path: str, recursive: bool) -> list[dict]:
    """Scans the given directory and returns a list of file information dictionaries."""
    base_path = Path(path)

    # Resolve against SANDBOX_ROOT to prevent directory traversal (../ attacks)
    resolved_path = base_path.resolve()

    check_path_validity(resolved_path)
    
    results: list[dict] = []


    def scan(current_path: Path):

        for entry in current_path.iterdir():

            stat = entry.stat()
            results.append(
                {
                    "name": entry.name,
                    "path": str(entry.resolve()),
                    "extension": entry.suffix if entry.is_file() else None,
                    "size_bytes": stat.st_size,
                    "is_directory": entry.is_dir(),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime),
                }
            )

            if recursive and entry.is_dir():
                scan(entry)
        
    
    scan(resolved_path)
    return results