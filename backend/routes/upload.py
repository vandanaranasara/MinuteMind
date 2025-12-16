from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.services.audio_transcribe import transcribe_audio
from backend.core.config import settings
from backend.schemas import UploadResponse
import os
import uuid

router = APIRouter(prefix="/upload", tags=["Upload Audio"])

AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".flac", ".ogg")

@router.post("", response_model=UploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(AUDIO_EXTS):
        raise HTTPException(status_code=400, detail="Only audio files are supported (mp3/wav/m4a/flac/ogg)")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    dest = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(dest, "wb") as f:
        f.write(await file.read())

    try:
        transcript = transcribe_audio(dest)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    return JSONResponse(content={
        "file_id": file_id,
        "filename": file.filename,
        "transcript": transcript
    })
