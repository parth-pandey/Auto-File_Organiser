# Revision — Auto File Organiser

A compact summary of the commands, Python code, and FastAPI concepts you've asked about so far ✅

---

## 1) pip install -r requirements.txt 🔧
- Command breakdown:
  - `pip` — the Python package installer (use `python -m pip` to be explicit about interpreter).
  - `install` — the subcommand that installs packages.
  - `-r` — read package specifiers from a file.
  - `requirements.txt` — file listing packages, one per line (e.g. `fastapi`, `uvicorn[standard]`, `pydantic`).
- Tip: update pip with `python -m pip install --upgrade pip` (you saw the notice earlier).

---

## 2) Filesystem commands: mkdir, touch, paths 🗂️
- `mkdir -p app/schemas` — creates `app` and `app/schemas` if needed; `-p` avoids errors if parents already exist.
  - Unix example: `mkdir -p app/schemas/models/controllers`
  - Windows cmd: `mkdir app\schemas\models\controllers` (cmd creates parents by default).
- `touch app/schemas/__init__.py` — creates an empty file or updates timestamps (Unix). Windows alternatives:
  - cmd: `type nul > app\schemas\__init__.py`
  - PowerShell: `New-Item -ItemType File -Path 'app/schemas/__init__.py' -Force`
- `app/schemas` is a path with nested folders — yes, you can create multiple nested levels at once.

---

## 3) `__init__.py` (why the name?) 🧩
- `__init__.py` is a "dunder" (double underscore) file executed when the package is imported.
- Historically required to mark a directory as a package; still useful to run package-level initialization or export `__all__`.
- Python 3.3+ supports implicit namespace packages (no file required), but using `__init__.py` is common practice.

---

## 4) Code & typing — `results: list[dict] = []` vs `results = []` 📝
- `results: list[dict] = []` assigns an empty list and *annotates* its type (helpful for mypy/Pyright and IDEs).
- `results = []` creates an empty list, but no explicit static type info is provided.
- Runtime behavior: both are the same (annotations are not enforced at runtime).
- Note: `list[dict]` requires Python 3.9+; older Python needs `from typing import List, Dict`.

---

## 5) Mutable default & shared-state pitfalls ⚠️
- Problem: default arguments are evaluated once at function definition time — mutable defaults get shared across calls.
- Function example (pitfall):
```python
def append_item(item, lst=[]):
    lst.append(item)
    return lst

print(append_item(1))  # [1]
print(append_item(2))  # [1, 2]  <-- unexpected
```
- Correct pattern:
```python
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```
- Class example (pitfall):
```python
class Collector:
    items = []  # shared by all instances
```
- Use instance attributes instead (`self.items = []` in `__init__`).

---

## 6) `str(entry.resolve())` and symlinks / absolute paths 📁
- `entry` is a `pathlib.Path`.
- `entry.resolve()` returns an absolute `Path` with symlinks resolved (i.e., the final target path).
- `str(...)` converts the `Path` to a string path (e.g., `C:\Users\...\file.txt`).
- Absolute path = full path from filesystem root; relative path depends on current working directory.
- Symlink = a filesystem reference (like a shortcut) that points to another file/directory.

---

## 7) `datetime.fromtimestamp(stat.st_mtime)` ⏱️
- `stat.st_mtime` is last-modified time in seconds since epoch (float).
- `datetime.fromtimestamp(...)` converts that into a naive `datetime` in local time.
- For UTC: use `datetime.utcfromtimestamp(...)` or `datetime.fromtimestamp(..., tz=timezone.utc)`.

---

## 8) FastAPI basics — routers, tags, and endpoints 🚀
- `APIRouter` groups routes by feature; create it with `APIRouter(prefix="/files", tags=["files"])`.
  - `prefix` applies to every route in the router (`/files` + route path).
  - `tags` are used in OpenAPI docs (Swagger/Redoc) for grouping; changing the tag name only affects docs, not runtime.
- Router-level vs route-level tags:
  - Router-level tags provide defaults for all routes in that router.
  - Route-level tags (e.g., `@router.get(..., tags=["public"])`) apply to the single route and do not merge automatically.
- Example endpoint:
```python
@router.get("", response_model=list[FileInfo])
def list_files(path: str = Query(..., description="Directory path to scan")):
    try:
        raw_files = scan_directory(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return raw_files
```
  - `response_model` tells FastAPI to validate/serialize with Pydantic.
  - `Query(..., description=...)` declares a required query parameter with docs.
  - `HTTPException` produces an HTTP error response with a status and message.

---

## 9) Application & ASGI server details 🧭
- In `main.py`:
  - `app = FastAPI(title="Auto File Organiser")` creates the ASGI app.
  - `app.include_router(files_router)` mounts router routes.
- ASGI app = an async callable with signature `(scope, receive, send)` supporting `http`, `websocket`, and `lifespan` events — enables async concurrency and WebSocket handling.
- `uvicorn app.main:app --reload` runs the ASGI app with Uvicorn; `--reload` auto restarts on code changes (dev only).
- Prefer `python -m uvicorn app.main:app --reload` to ensure correct interpreter.

---

## 10) uvicorn & CLI 🖥️
- `uvicorn` is a lightweight ASGI server for running FastAPI/Starlette apps.
- CLI = Command-Line Interface (text-based input to run commands and pass options).
- Default server address: `127.0.0.1:8000`. FastAPI docs available at `/docs` and `/redoc` when app is running.

---

## Quick Tips & Notes ✨
- Run `pip` inside a virtual environment (you have `(venv)` in your prompt) so packages install locally.
- `.gitignore` commonly includes `__pycache__/`, `*.pyc`, `.env`, `venv/`, `.venv/` (you have these already).
- Use type annotations to improve editor help and static checks, but types are not enforced at runtime.

---

