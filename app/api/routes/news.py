from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.news import News, NewsSearchParams, NewsSearchResponse
from ...services.news_service import get_news, get_user_news, search_news
from ...core.auth import get_current_user
from ...db.models import User

router = APIRouter()

@router.post("/search", response_model=NewsSearchResponse)
async def search_news_endpoint(
    params: NewsSearchParams,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    키워드로 뉴스를 검색합니다.
    """
    results = await search_news(db, params, current_user.id)
    return NewsSearchResponse(
        total_count=len(results),
        results=results
    )

@router.get("/{news_id}", response_model=News)
def get_news_endpoint(
    news_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 뉴스의 상세 정보를 조회합니다.
    """
    news = get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    if news.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this news")
    return news

@router.get("/", response_model=List[News])
def get_user_news_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자가 수집한 뉴스 목록을 조회합니다.
    """
    return get_user_news(db, current_user.id, skip, limit) 