from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostOutput(BaseModel):
    post_id: int
    post_url: str
    post_text: Optional[str]
    post_created_at: Optional[datetime]
    post_rating: int
    is_deleted: bool
    related_to: Optional[str]
    topic_id: int
    author_id: int
