from fastapi import FastAPI
from app.api.files import router as files_router

app = FastAPI(title="Auto File Organiser")

app.include_router(files_router)