from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class NewsBase(BaseModel):
    source: str
    title: str
    content: str
    url: str
    published_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class NewsCreate(NewsBase):
    pass

class NewsUpdate(NewsBase):
    pass

class NewsInDBBase(NewsBase):
    id: int
    user_id: int
    collected_at: datetime

    class Config:
        from_attributes = True

class News(NewsInDBBase):
    pass

class NewsSearchParams(BaseModel):
    keyword: str
    num_results: Optional[int] = 10
    date_range: Optional[str] = None
    sources: Optional[list[str]] = ["google", "naver", "sk_hynix", "samsung_semiconductor"]

class NewsSearchResponse(BaseModel):
    total_count: int
    results: list[News] 