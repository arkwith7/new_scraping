from typing import List, Dict, Optional
from googleapiclient.discovery import build
from .base import BaseScraper

class GoogleSearchScraper(BaseScraper):
    """구글 검색 API를 사용하는 스크래퍼"""
    
    def __init__(self, api_key: str, cx: str):
        """
        Args:
            api_key (str): Google API 키
            cx (str): Custom Search Engine ID
        """
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cx = cx
    
    def search(self, keyword: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict]:
        try:
            # 검색 쿼리 구성
            query = {
                'q': keyword,
                'cx': self.cx,
                'num': min(num_results, 10),  # Google API는 한 번에 최대 10개 결과만 반환
                'dateRestrict': date_range if date_range else None
            }
            
            # 검색 실행
            result = self.service.cse().list(**query).execute()
            
            # 결과 처리
            items = result.get('items', [])
            return self._process_results(items)
            
        except Exception as e:
            print(f"Error in Google search: {str(e)}")
            return []
    
    def _process_results(self, items: List[Dict]) -> List[Dict]:
        """검색 결과를 처리합니다."""
        processed_results = []
        for item in items:
            processed_results.append({
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', ''),
                'date': self._format_date(
                    item.get('pagemap', {})
                    .get('metatags', [{}])[0]
                    .get('article:published_time', '')
                ),
                'source': 'google'
            })
        return processed_results
