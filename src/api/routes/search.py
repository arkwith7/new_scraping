from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ...scrapers.search_manager import SearchManager
from ...analyzers.text_analyzer import TextAnalyzer
from ...analyzers.topic_modeling import TopicModeler
from ...services.search_service import GoogleSearchService, NaverSearchService
from ...utils.storage import save_search_results

router = APIRouter()

# 의존성 주입을 위한 함수
def get_search_manager():
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    return SearchManager(
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        google_cx=os.getenv('GOOGLE_CX'),
        naver_client_id=os.getenv('NAVER_CLIENT_ID'),
        naver_client_secret=os.getenv('NAVER_CLIENT_SECRET')
    )

# 요청 모델
class SearchRequest(BaseModel):
    keyword: str
    num_results: Optional[int] = 10
    date_range: Optional[str] = None
    sources: Optional[List[str]] = ["google", "naver"]
    save_to_file: Optional[bool] = True

class AnalyzeRequest(BaseModel):
    texts: List[str]

class TopicModelingRequest(BaseModel):
    texts: List[str]
    num_topics: Optional[int] = 5
    passes: Optional[int] = 10

# 응답 모델
class SearchResponse(BaseModel):
    results: List[Dict]
    total_count: int
    saved_files: Optional[List[str]] = []

class AnalysisResponse(BaseModel):
    total_texts: int
    total_words: int
    unique_words: int
    keywords: List[tuple]
    word_frequency: dict

class TopicModelingResponse(BaseModel):
    topics: List[dict]
    evaluation: dict

# 엔드포인트
@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    검색 API
    
    Args:
        request (SearchRequest): 검색 요청 파라미터
        
    Returns:
        SearchResponse: 검색 결과
    """
    try:
        results = []
        saved_files = []
        
        if "google" in request.sources:
            google_service = GoogleSearchService()
            google_results = await google_service.search(
                keyword=request.keyword,
                num_results=request.num_results,
                date_range=request.date_range
            )
            results.extend(google_results)
            
            if request.save_to_file and google_results:
                filepath = save_search_results(google_results, "google", request.keyword)
                saved_files.append(filepath)
        
        if "naver" in request.sources:
            naver_service = NaverSearchService()
            naver_results = await naver_service.search(
                keyword=request.keyword,
                num_results=request.num_results,
                date_range=request.date_range
            )
            results.extend(naver_results)
            
            if request.save_to_file and naver_results:
                filepath = save_search_results(naver_results, "naver", request.keyword)
                saved_files.append(filepath)
        
        return SearchResponse(
            results=results,
            total_count=len(results),
            saved_files=saved_files if request.save_to_file else []
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"검색 중 오류 발생: {str(e)}"
        )

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_texts(request: AnalyzeRequest):
    """텍스트를 분석합니다."""
    try:
        analyzer = TextAnalyzer()
        results = analyzer.analyze_texts(request.texts)
        return AnalysisResponse(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topic-modeling", response_model=TopicModelingResponse)
async def topic_modeling(request: TopicModelingRequest):
    """토픽 모델링을 수행합니다."""
    try:
        modeler = TopicModeler()
        modeler.prepare_corpus(request.texts)
        modeler.train_model(
            num_topics=request.num_topics,
            passes=request.passes
        )
        
        topics = modeler.get_topics()
        evaluation = modeler.evaluate_model()
        
        return TopicModelingResponse(
            topics=topics,
            evaluation=evaluation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
