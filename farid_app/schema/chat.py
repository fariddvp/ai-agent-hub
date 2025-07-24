from typing import List, Optional
from pydantic import BaseModel


class ChatSchema(BaseModel):
    q: str
    n: Optional[int] = 7
    d: Optional[float] = 0
    stream: Optional[bool] = False
    title: Optional[str] = ""
    conversation_id: Optional[str] = ""
    turn_id: Optional[str] = ""
    city: Optional[str] = ""
    region: Optional[str] = ""
    country: Optional[str] = ""
    country_code: Optional[str] = ""
    timezone: Optional[str] = ""
    images: Optional[List[str]] = []
    files: Optional[List[str]] = []
    create_new: Optional[bool] = False