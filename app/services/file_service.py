from pathlib import Path
from datetime import datetime
from app.core.config import SANDBOX_ROOT


def scan_directory(path: str) -> list[dict]:
    """Scans the given directory and returns a list of file information dictionaries."""
    base_path = Path(path)

    # Resolve against SANDBOX_ROOT to prevent directory traversal (../ attacks)
    resolved_path = base_path.resolve()

    if not resolved_path.is_relative_to(SANDBOX_ROOT):
        raise ValueError("Access to the specified path is not allowed")

    if not resolved_path.exists():
        raise ValueError("Path does not exist")
    
    if not resolved_path.is_dir():
        raise ValueError("Path is not a directory")
    
    results: list[dict] = []

    for entry in resolved_path.iterdir():
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
    
    return results