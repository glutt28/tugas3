from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    review_text: str

class ReviewResponse(BaseModel):
    id: int
    review_text: str
    sentiment: str
    key_points: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

