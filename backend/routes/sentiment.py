from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.llm_client import LLMClient
from backend.services.prompt_builder import build_sentiment_prompt

router = APIRouter(prefix="/sentiment", tags=["Sentiment"])

class SentimentRequest(BaseModel):
    transcript: str

@router.post("")
async def get_sentiment(req: SentimentRequest):
    llm = LLMClient()
    prompt = build_sentiment_prompt(req.transcript)
    text = llm.complete(prompt)
    # Expect JSON mapping speaker->sentiment
    import json
    try:
        return json.loads(text)
    except:
        # try simple parse
        import re
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        return {"error": "Could not parse sentiment output", "raw": text}
