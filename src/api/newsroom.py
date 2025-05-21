from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from ..scrapers.newsroom_scraper import SKHynixNewsScraper, SamsungSemiconNewsScraper

router = APIRouter()

class NewsroomSearchRequest(BaseModel):
    keyword: str
    num_results: Optional[int] = 10
    date_range: Optional[str] = None
    sources: Optional[List[str]] = ["sk_hynix", "samsung_semiconductor"]

class NewsroomSearchResponse(BaseModel):
    articles: List[Dict]
    total_count: int

@router.post("/newsroom/search", response_model=NewsroomSearchResponse)
async def search_newsroom(request: NewsroomSearchRequest):
    """
    뉴스룸 기사 검색 API
    
    Args:
        request (NewsroomSearchRequest): 검색 요청 파라미터
        
    Returns:
        NewsroomSearchResponse: 검색 결과
    """
    try:
        articles = []
        
        if "sk_hynix" in request.sources:
            sk_scraper = SKHynixNewsScraper()
            try:
                sk_articles = sk_scraper.search(
                    keyword=request.keyword,
                    num_results=request.num_results,
                    date_range=request.date_range
                )
                articles.extend(sk_articles)
            finally:
                sk_scraper.cleanup()
        
        if "samsung_semiconductor" in request.sources:
            samsung_scraper = SamsungSemiconNewsScraper()
            try:
                samsung_articles = samsung_scraper.search(
                    keyword=request.keyword,
                    num_results=request.num_results,
                    date_range=request.date_range
                )
                articles.extend(samsung_articles)
            finally:
                samsung_scraper.cleanup()
        
        return NewsroomSearchResponse(
            articles=articles,
            total_count=len(articles)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"뉴스룸 검색 중 오류 발생: {str(e)}"
        ) 