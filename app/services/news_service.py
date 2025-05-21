from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..db.models import NewsData, APIUsage
from ..schemas.news import NewsCreate, NewsSearchParams
from .search_service import GoogleSearchService, NaverSearchService
from .newsroom_service import SKHynixNewsService, SamsungSemiconNewsService

def create_news(db: Session, news: NewsCreate, user_id: int) -> NewsData:
    db_news = NewsData(
        user_id=user_id,
        source=news.source,
        title=news.title,
        content=news.content,
        url=news.url,
        published_date=news.published_date,
        metadata=news.metadata
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def get_news(db: Session, news_id: int) -> Optional[NewsData]:
    return db.query(NewsData).filter(NewsData.id == news_id).first()

def get_user_news(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[NewsData]:
    return db.query(NewsData)\
        .filter(NewsData.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def update_api_usage(db: Session, user_id: int, endpoint: str) -> None:
    usage = APIUsage(
        user_id=user_id,
        endpoint=endpoint,
        request_count=1,
        date=datetime.utcnow()
    )
    db.add(usage)
    db.commit()

async def search_news(
    db: Session,
    params: NewsSearchParams,
    user_id: int
) -> List[NewsData]:
    results = []
    
    if "google" in params.sources:
        google_service = GoogleSearchService()
        google_results = await google_service.search(
            keyword=params.keyword,
            num_results=params.num_results,
            date_range=params.date_range
        )
        for result in google_results:
            news = NewsCreate(
                source="google",
                title=result["title"],
                content=result.get("content", ""),
                url=result["url"],
                published_date=result.get("published_date"),
                metadata=result
            )
            db_news = create_news(db, news, user_id)
            results.append(db_news)
        update_api_usage(db, user_id, "google_search")
    
    if "naver" in params.sources:
        naver_service = NaverSearchService()
        naver_results = await naver_service.search(
            keyword=params.keyword,
            num_results=params.num_results,
            date_range=params.date_range
        )
        for result in naver_results:
            news = NewsCreate(
                source="naver",
                title=result["title"],
                content=result.get("content", ""),
                url=result["url"],
                published_date=result.get("published_date"),
                metadata=result
            )
            db_news = create_news(db, news, user_id)
            results.append(db_news)
        update_api_usage(db, user_id, "naver_search")
    
    if "sk_hynix" in params.sources:
        sk_service = SKHynixNewsService()
        sk_results = await sk_service.search(
            keyword=params.keyword,
            num_results=params.num_results,
            date_range=params.date_range
        )
        for result in sk_results:
            news = NewsCreate(
                source="sk_hynix",
                title=result["title"],
                content=result.get("content", ""),
                url=result["url"],
                published_date=result.get("published_date"),
                metadata=result
            )
            db_news = create_news(db, news, user_id)
            results.append(db_news)
        update_api_usage(db, user_id, "sk_hynix_search")
    
    if "samsung_semiconductor" in params.sources:
        samsung_service = SamsungSemiconNewsService()
        samsung_results = await samsung_service.search(
            keyword=params.keyword,
            num_results=params.num_results,
            date_range=params.date_range
        )
        for result in samsung_results:
            news = NewsCreate(
                source="samsung_semiconductor",
                title=result["title"],
                content=result.get("content", ""),
                url=result["url"],
                published_date=result.get("published_date"),
                metadata=result
            )
            db_news = create_news(db, news, user_id)
            results.append(db_news)
        update_api_usage(db, user_id, "samsung_semiconductor_search")
    
    return results 