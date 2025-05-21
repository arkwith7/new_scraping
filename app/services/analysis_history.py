from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import AnalysisHistory, ComparisonHistory, SummaryHistory
from app.schemas.analysis import (
    AnalysisHistoryCreate,
    ComparisonHistoryCreate,
    SummaryHistoryCreate
)

class AnalysisHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_analysis_history(
        self,
        user_id: int,
        analysis_type: str,
        text: str,
        result: dict
    ) -> AnalysisHistory:
        history = AnalysisHistory(
            user_id=user_id,
            analysis_type=analysis_type,
            text=text,
            result=result
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_analysis_history(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[AnalysisHistory]:
        return self.db.query(AnalysisHistory)\
            .filter(AnalysisHistory.user_id == user_id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def create_comparison_history(
        self,
        user_id: int,
        text1: str,
        text2: str,
        result: dict
    ) -> ComparisonHistory:
        history = ComparisonHistory(
            user_id=user_id,
            text1=text1,
            text2=text2,
            result=result
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_comparison_history(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[ComparisonHistory]:
        return self.db.query(ComparisonHistory)\
            .filter(ComparisonHistory.user_id == user_id)\
            .order_by(ComparisonHistory.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def create_summary_history(
        self,
        user_id: int,
        text: str,
        max_length: Optional[int],
        result: dict
    ) -> SummaryHistory:
        history = SummaryHistory(
            user_id=user_id,
            text=text,
            max_length=max_length,
            result=result
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_summary_history(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[SummaryHistory]:
        return self.db.query(SummaryHistory)\
            .filter(SummaryHistory.user_id == user_id)\
            .order_by(SummaryHistory.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all() 