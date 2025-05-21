from typing import List, Dict, Optional
import requests
from .base import BaseScraper

class NaverSearchScraper(BaseScraper):
    """네이버 검색 API를 사용하는 스크래퍼"""
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Args:
            client_id (str): Naver API Client ID
            client_secret (str): Naver API Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://openapi.naver.com/v1/search/news.json"
    
    def search(self, keyword: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict]:
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        
        params = {
            'query': keyword,
            'display': min(num_results, 100),  # Naver API는 한 번에 최대 100개 결과 반환
            'start': 1,
            'sort': 'date'
        }
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            
            results = response.json()
            return self._process_results(results.get('items', []))
            
        except Exception as e:
            print(f"Error in Naver search: {str(e)}")
            return []
    
    def _process_results(self, items: List[Dict]) -> List[Dict]:
        """검색 결과를 처리합니다."""
        processed_results = []
        for item in items:
            processed_results.append({
                'title': item.get('title', '').replace('<b>', '').replace('</b>', ''),
                'link': item.get('link', ''),
                'snippet': item.get('description', '').replace('<b>', '').replace('</b>', ''),
                'date': self._format_date(item.get('pubDate', '')),
                'source': 'naver'
            })
        return processed_results
