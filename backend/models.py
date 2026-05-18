from pydantic import BaseModel
from typing import Optional

class NoticeCreate(BaseModel):
    title: str
    content: str
    category: str = "일반"
    is_pinned: bool = False

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_pinned: Optional[bool] = None

class ActivityCreate(BaseModel):
    team_id: int
    activity_date: str        # "2026-05-11"
    title: str
    description: Optional[str] = None
    attendees: int = 0
    amount_used: int = 0

class ActivityUpdate(BaseModel):
    activity_date: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    attendees: Optional[int] = None
    amount_used: Optional[int] = None

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    task: Optional[str] = None
    card_status: Optional[str] = None
    card_submissions: Optional[dict] = None
