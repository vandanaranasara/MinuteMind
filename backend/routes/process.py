from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_client import LLMClient
from backend.services.prompt_builder import build_prompt
from backend.utils.validators import ensure_json_serializable
from backend.schemas import ProcessRequest, ProcessResponse
import json
import logging
import re


router = APIRouter(prefix="/process", tags=["Process"])
logger = logging.getLogger("process_router")

class RawRequest(ProcessRequest):
    pass

@router.post("", response_model=ProcessResponse)
async def process_meeting(req: RawRequest):
    """
    Accepts:
    {
      "transcript": "...",
      "meeting_title": "...",
      "meeting_date": "2025-12-18",
      "include_speakers": true,
      "include_sentiment": true,
      "include_timeline": true,
      "language": "english"
    }
    """
    if not req.transcript or len(req.transcript.strip()) < 10:
        raise HTTPException(status_code=400, detail="Transcript is too short or empty.")

    # Detect timestamps like 00:12 or 1:05:33
    has_timestamps = bool(
    re.search(
        r"\[\s*\d+(\.\d+)?\s*-\s*\d+(\.\d+)?\s*\]|\b\d{1,2}:\d{2}(:\d{2})?\b",
        req.transcript
    )
)

    # Only allow timeline if user asked AND transcript has timestamps
    include_timeline_effective = req.include_timeline and has_timestamps

    prompt = build_prompt(
        transcript=req.transcript,
        meeting_title=req.meeting_title,
        meeting_date=req.meeting_date,
        include_speakers=req.include_speakers,
        include_sentiment=req.include_sentiment,
        include_timeline=include_timeline_effective,
        language=req.language
    )

    llm = LLMClient()
    output_text = llm.complete(prompt)

    # The model MUST return JSON. We attempt to parse.
    try:
        parsed = json.loads(output_text)
    except Exception as e:
        logger.error("LLM returned non-JSON. Try to extract JSON portion.")
        # fallback attempt: try to locate first { ... } chunk
        match = re.search(r"\{.*\}", output_text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except Exception as e2:
                raise HTTPException(status_code=500, detail=f"Failed to parse model JSON: {str(e2)}")
        else:
            raise HTTPException(status_code=500, detail="LLM did not return JSON.")

    # Basic validation
    ensure_json_serializable(parsed)

    # Enforce empty timeline when we disabled it
    if not include_timeline_effective:
        parsed["timeline"] = []
    
    # Enforce empty sentiment when we disabled it
    if not req.include_sentiment:
        parsed["speaker_sentiment"] = {}
    
    parsed["meeting_title"] = req.meeting_title
    parsed["meeting_date"] = req.meeting_date

    return parsed

