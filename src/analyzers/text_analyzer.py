from typing import List, Dict, Tuple
from collections import Counter
from kiwipiepy import Kiwi
import numpy as np
from ..utils.text_preprocessing import TextPreprocessor

class TextAnalyzer:
    """텍스트 분석을 수행하는 클래스"""
    
    def __init__(self):
        self.kiwi = Kiwi()
        self.preprocessor = TextPreprocessor()
    
    def analyze_texts(self, texts: List[str]) -> Dict:
        """
        여러 텍스트를 분석합니다.
        
        Args:
            texts (List[str]): 분석할 텍스트 리스트
            
        Returns:
            Dict: 분석 결과
        """
        # 텍스트 전처리
        processed_texts = [self.preprocessor.preprocess(text) for text in texts]
        
        # 형태소 분석
        morphemes = []
        for text in processed_texts:
            result = self.kiwi.analyze(text)
            morphemes.extend([token.form for token in result[0][0]])
        
        # 빈도 분석
        word_freq = Counter(morphemes)
        
        # 키워드 추출 (상위 20개)
        keywords = word_freq.most_common(20)
        
        return {
            'total_texts': len(texts),
            'total_words': len(morphemes),
            'unique_words': len(word_freq),
            'keywords': keywords,
            'word_frequency': dict(word_freq)
        }
    
    def get_similarity(self, text1: str, text2: str) -> float:
        """
        두 텍스트 간의 유사도를 계산합니다.
        
        Args:
            text1 (str): 첫 번째 텍스트
            text2 (str): 두 번째 텍스트
            
        Returns:
            float: 유사도 점수 (0~1)
        """
        # 텍스트 전처리
        text1 = self.preprocessor.preprocess(text1)
        text2 = self.preprocessor.preprocess(text2)
        
        # 형태소 분석
        result1 = self.kiwi.analyze(text1)
        result2 = self.kiwi.analyze(text2)
        
        # 단어 집합 생성
        words1 = set(token.form for token in result1[0][0])
        words2 = set(token.form for token in result2[0][0])
        
        # Jaccard 유사도 계산
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
