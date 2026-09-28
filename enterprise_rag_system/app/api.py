from pathlib import Path
from uuid import uuid4
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.config import settings
from src.ingestion import load_document
from src.vectorstore import build_index
from src.rag import RAGPipeline


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


class Question(BaseModel):
    question: str


# Background indexing
executor = ThreadPoolExecutor(max_workers=1)

jobs = {}
jobs_lock = Lock()


def update_job(job_id: str, **updates):
    with jobs_lock:
        jobs[job_id].update(updates)


def process_document(job_id: str, file_path: str):
    try:
        update_job(
            job_id,
            status="processing",
            stage="Extracting and chunking document",
        )

        chunks = load_document(file_path)

        update_job(
            job_id,
            stage="Building FAISS vector index",
            chunks=len(chunks),
        )

        build_index(chunks)

        update_job(
            job_id,
            status="completed",
            stage="Indexing completed",
            chunks=len(chunks),
        )

    except Exception as exc:
        update_job(
            job_id,
            status="failed",
            stage="Indexing failed",
            error=str(exc),
        )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }


@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "Filename is required.")

    suffix = Path(file.filename).suffix.lower()

    if suffix not in {".pdf", ".docx", ".txt", ".md"}:
        raise HTTPException(
            400,
            "Supported files: PDF, DOCX, TXT, MD",
        )

    safe_filename = Path(file.filename).name
    target = settings.upload_dir / safe_filename

    target.write_bytes(await file.read())

    job_id = str(uuid4())

    with jobs_lock:
        jobs[job_id] = {
            "job_id": job_id,
            "filename": safe_filename,
            "status": "queued",
            "stage": "Waiting to start",
            "chunks": 0,
            "error": None,
        }

    executor.submit(
        process_document,
        job_id,
        str(target),
    )

    return {
        "job_id": job_id,
        "filename": safe_filename,
        "status": "queued",
        "message": "Document uploaded. Indexing started in the background.",
    }


@app.get("/documents/status/{job_id}")
def document_status(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)

    if not job:
        raise HTTPException(
            404,
            "Job not found.",
        )

    return job


@app.post("/ask")
def ask(payload: Question):
    try:
        result = RAGPipeline().answer(payload.question)

        return JSONResponse(
            content=result,
            media_type="application/json; charset=utf-8",
        )

    except FileNotFoundError as exc:
        raise HTTPException(409, str(exc))
