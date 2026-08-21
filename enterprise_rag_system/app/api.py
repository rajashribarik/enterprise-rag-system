from pathlib import Path

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


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }


@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in {".pdf", ".docx", ".txt", ".md"}:
        raise HTTPException(
            400,
            "Supported files: PDF, DOCX, TXT, MD",
        )

    target = settings.upload_dir / Path(file.filename).name
    target.write_bytes(await file.read())

    chunks = load_document(str(target))
    build_index(chunks)

    return {
        "filename": target.name,
        "chunks_indexed": len(chunks),
    }


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