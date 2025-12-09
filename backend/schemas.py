from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class BaseResponse(BaseModel):
    pass

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    transcript: str

class ActionItem(BaseModel):
    task: str
    assigned_to: Optional[str] = None
    deadline: Optional[str] = None

class TimelineItem(BaseModel):
    timestamp: str
    topic: str

class ProcessRequest(BaseModel):
    transcript: str
    meeting_title: Optional[str] = None
    include_speakers: bool = True
    include_sentiment: bool = True
    include_timeline: bool = True
    language: str = "english"

class ProcessResponse(BaseModel):
    summary_short: List[str]
    summary_detailed: str
    discussion_flow: List[str]
    timeline: List[TimelineItem]
    action_items: List[ActionItem]
    speaker_sentiment: Dict[str, str]
