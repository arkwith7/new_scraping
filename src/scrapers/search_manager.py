from typing import List, Dict, Optional
from .google_search import GoogleSearchScraper
from .naver_search import NaverSearchScraper

class SearchManager:
    """검색 API들을 관리하는 클래스"""
    
    def __init__(self, google_api_key: str, google_cx: str, naver_client_id: str, naver_client_secret: str):
        """
        Args:
            google_api_key (str): Google API 키
            google_cx (str): Google Custom Search Engine ID
            naver_client_id (str): Naver API Client ID
            naver_client_secret (str): Naver API Client Secret
        """
        self.google_scraper = GoogleSearchScraper(google_api_key, google_cx)
        self.naver_scraper = NaverSearchScraper(naver_client_id, naver_client_secret)
    
    def search_all(self, keyword: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict]:
        """
        모든 검색 API를 사용하여 검색을 수행합니다.
        
        Args:
            keyword (str): 검색할 키워드
            num_results (int): 각 API에서 반환할 결과 수
            date_range (Optional[str]): 검색 기간
            
        Returns:
            List[Dict]: 통합된 검색 결과 리스트
        """
        results = []
        
        # 구글 검색
        google_results = self.google_scraper.search(keyword, num_results, date_range)
        results.extend(google_results)
        
        # 네이버 검색
        naver_results = self.naver_scraper.search(keyword, num_results, date_range)
        results.extend(naver_results)
        
        # 날짜순으로 정렬
        results.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return results
