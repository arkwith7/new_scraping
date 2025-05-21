from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.analysis import AnalysisResult, AnalysisCreate, TextAnalysisRequest, TextComparisonRequest, TextSummaryRequest, AnalysisHistory, ComparisonHistory, SummaryHistory
from ...services.analysis_service import NewsAnalysisService
from ...services.news_service import get_user_news
from ...core.auth import get_current_user
from ...db.models import User
from ...services.ai_agent import TextAnalysisAgent
from ...services.analysis_history import AnalysisHistoryService

router = APIRouter()
ai_agent = TextAnalysisAgent()

@router.post("/analyze", response_model=AnalysisResult)
def analyze_news_endpoint(
    analysis_create: AnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    선택한 뉴스 데이터에 대한 분석을 수행합니다.
    """
    # 뉴스 데이터 조회
    news_list = []
    for news_id in analysis_create.news_ids:
        news = get_user_news(db, current_user.id, news_id)
        if not news:
            raise HTTPException(status_code=404, detail=f"News {news_id} not found")
        news_list.append(news)
    
    # 분석 수행
    analysis_service = NewsAnalysisService(db)
    result = analysis_service.analyze_news(news_list)
    
    return result

@router.get("/{analysis_id}", response_model=AnalysisResult)
def get_analysis_endpoint(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 분석 결과를 조회합니다.
    """
    analysis_service = NewsAnalysisService(db)
    result = analysis_service.get_analysis_result(analysis_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    if result.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this analysis")
    
    return result

@router.get("/", response_model=List[AnalysisResult])
def get_user_analysis_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자의 분석 결과 목록을 조회합니다.
    """
    analysis_service = NewsAnalysisService(db)
    return analysis_service.get_user_analysis_results(current_user.id, skip, limit)

@router.post("/analyze")
async def analyze_text(
    request: TextAnalysisRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """텍스트 분석"""
    result = await ai_agent.analyze_text(
        text=request.text,
        analysis_type=request.analysis_type
    )
    
    # 분석 결과 저장
    history_service = AnalysisHistoryService(db)
    history_service.create_analysis_history(
        user_id=current_user.id,
        analysis_type=request.analysis_type,
        text=request.text,
        result=result
    )
    
    return result

@router.post("/compare")
async def compare_texts(
    request: TextComparisonRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """텍스트 비교"""
    result = await ai_agent.compare_texts(
        text1=request.text1,
        text2=request.text2
    )
    
    # 비교 결과 저장
    history_service = AnalysisHistoryService(db)
    history_service.create_comparison_history(
        user_id=current_user.id,
        text1=request.text1,
        text2=request.text2,
        result=result
    )
    
    return result

@router.post("/summarize")
async def summarize_text(
    request: TextSummaryRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """텍스트 요약"""
    result = await ai_agent.summarize_text(
        text=request.text,
        max_length=request.max_length
    )
    
    # 요약 결과 저장
    history_service = AnalysisHistoryService(db)
    history_service.create_summary_history(
        user_id=current_user.id,
        text=request.text,
        max_length=request.max_length,
        result=result
    )
    
    return result

@router.get("/history/analysis", response_model=List[AnalysisHistory])
def get_analysis_history(
    skip: int = 0,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """분석 히스토리 조회"""
    history_service = AnalysisHistoryService(db)
    return history_service.get_analysis_history(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.get("/history/comparison", response_model=List[ComparisonHistory])
def get_comparison_history(
    skip: int = 0,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """비교 히스토리 조회"""
    history_service = AnalysisHistoryService(db)
    return history_service.get_comparison_history(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.get("/history/summary", response_model=List[SummaryHistory])
def get_summary_history(
    skip: int = 0,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """요약 히스토리 조회"""
    history_service = AnalysisHistoryService(db)
    return history_service.get_summary_history(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    ) 