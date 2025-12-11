from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_client import LLMClient
from backend.services.prompt_builder import build_prompt
from backend.utils.validators import ensure_json_serializable
from backend.schemas import ProcessRequest, ProcessResponse
import json
import logging

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
      "include_speakers": true,
      "include_sentiment": true,
      "include_timeline": true,
      "language":"english"
    }
    """
    if not req.transcript or len(req.transcript.strip()) < 10:
        raise HTTPException(status_code=400, detail="Transcript is too short or empty.")

    prompt = build_prompt(
        transcript=req.transcript,
        meeting_title=req.meeting_title,
        include_speakers=req.include_speakers,
        include_sentiment=req.include_sentiment,
        include_timeline=req.include_timeline,
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
        import re
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
    # Optionally post-process timestamps, fill empty fields
    response_obj = parsed
    return response_obj
