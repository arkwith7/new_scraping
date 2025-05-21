from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class AnalysisBase(BaseModel):
    news_ids: List[int]

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResult(AnalysisBase):
    id: int
    user_id: int
    keywords: Dict[str, float]
    sentiment: Dict[str, float]
    topics: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        orm_mode = True

class AnalysisHistoryBase(BaseModel):
    user_id: int
    analysis_type: str
    text: str
    result: Dict

class AnalysisHistoryCreate(AnalysisHistoryBase):
    pass

class AnalysisHistory(AnalysisHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ComparisonHistoryBase(BaseModel):
    user_id: int
    text1: str
    text2: str
    result: Dict

class ComparisonHistoryCreate(ComparisonHistoryBase):
    pass

class ComparisonHistory(ComparisonHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SummaryHistoryBase(BaseModel):
    user_id: int
    text: str
    max_length: Optional[int]
    result: Dict

class SummaryHistoryCreate(SummaryHistoryBase):
    pass

class SummaryHistory(SummaryHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 