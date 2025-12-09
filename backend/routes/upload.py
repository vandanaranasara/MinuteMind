from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.schemas import UploadResponse
from backend.services.extraction import extract_text_from_file
from backend.core.config import settings
import os
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # validate file type
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt supported")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    dest = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(dest, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_file(dest)
    # For privacy: we can delete the raw file after extraction if configured
    # os.remove(dest)
    return JSONResponse(content={"file_id": file_id, "filename": file.filename, "transcript": text})
