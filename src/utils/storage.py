import json
import os
from datetime import datetime
from typing import Dict, List
import logging

def save_articles(articles: List[Dict], source: str) -> str:
    """
    수집된 기사를 JSON 파일로 저장합니다.
    
    Args:
        articles (List[Dict]): 저장할 기사 목록
        source (str): 기사 출처 (sk_hynix 또는 samsung_semiconductor)
        
    Returns:
        str: 저장된 파일 경로
    """
    try:
        # 저장 디렉토리 생성
        base_dir = os.path.join("data", "newsroom", source)
        os.makedirs(base_dir, exist_ok=True)
        
        # 파일명 생성 (날짜_시간.json)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.json"
        filepath = os.path.join(base_dir, filename)
        
        # JSON 파일로 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        logging.info(f"기사 {len(articles)}개가 {filepath}에 저장되었습니다.")
        return filepath
        
    except Exception as e:
        logging.error(f"기사 저장 중 오류 발생: {str(e)}")
        raise

def save_search_results(results: List[Dict], source: str, keyword: str) -> str:
    """
    검색 API 결과를 JSON 파일로 저장합니다.
    
    Args:
        results (List[Dict]): 저장할 검색 결과 목록
        source (str): 검색 출처 (google 또는 naver)
        keyword (str): 검색 키워드
        
    Returns:
        str: 저장된 파일 경로
    """
    try:
        # 저장 디렉토리 생성
        base_dir = os.path.join("data", "search", source)
        os.makedirs(base_dir, exist_ok=True)
        
        # 파일명 생성 (키워드_날짜_시간.json)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keyword = keyword.replace(" ", "_")
        filename = f"{safe_keyword}_{timestamp}.json"
        filepath = os.path.join(base_dir, filename)
        
        # 메타데이터 추가
        data = {
            "keyword": keyword,
            "source": source,
            "timestamp": timestamp,
            "total_count": len(results),
            "results": results
        }
        
        # JSON 파일로 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"검색 결과 {len(results)}개가 {filepath}에 저장되었습니다.")
        return filepath
        
    except Exception as e:
        logging.error(f"검색 결과 저장 중 오류 발생: {str(e)}")
        raise 