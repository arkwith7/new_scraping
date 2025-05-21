from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime

class BaseScraper(ABC):
    """기본 스크래퍼 클래스"""
    
    @abstractmethod
    def search(self, keyword: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict]:
        """
        키워드로 검색을 수행합니다.
        
        Args:
            keyword (str): 검색할 키워드
            num_results (int): 반환할 결과 수
            date_range (Optional[str]): 검색 기간 (예: 'd1', 'w1', 'm1', 'y1')
            
        Returns:
            List[Dict]: 검색 결과 리스트
        """
        pass
    
    def _format_date(self, date_str: str) -> str:
        """날짜 문자열을 포맷팅합니다."""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return date_str
