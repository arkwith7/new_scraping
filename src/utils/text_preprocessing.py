import re
from typing import List, Set
from kiwipiepy import Kiwi

class TextPreprocessor:
    """텍스트 전처리를 수행하는 클래스"""
    
    def __init__(self):
        self.kiwi = Kiwi()
        self.stop_words = self._load_stop_words()
    
    def _load_stop_words(self) -> Set[str]:
        """불용어 목록을 로드합니다."""
        # 기본 불용어 목록
        stop_words = {
            '이', '그', '저', '것', '수', '등', '및', '또는', '그리고', '하지만',
            '그러나', '그래서', '때문에', '위해', '대해', '관련', '따른', '따라',
            '통해', '의해', '대한', '있는', '없는', '있는', '없는', '있는', '없는'
        }
        return stop_words
    
    def preprocess(self, text: str) -> str:
        """
        텍스트를 전처리합니다.
        
        Args:
            text (str): 전처리할 텍스트
            
        Returns:
            str: 전처리된 텍스트
        """
        # 소문자 변환
        text = text.lower()
        
        # 특수문자 제거
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 숫자 제거
        text = re.sub(r'\d+', ' ', text)
        
        # 여러 공백을 하나로 변환
        text = re.sub(r'\s+', ' ', text)
        
        # 앞뒤 공백 제거
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        텍스트를 토큰화합니다.
        
        Args:
            text (str): 토큰화할 텍스트
            
        Returns:
            List[str]: 토큰 리스트
        """
        # 텍스트 전처리
        text = self.preprocess(text)
        
        # 형태소 분석
        result = self.kiwi.analyze(text)
        
        # 명사, 동사, 형용사만 추출
        tokens = []
        for token in result[0][0]:
            if token.tag.startswith(('NN', 'VV', 'VA')) and token.form not in self.stop_words:
                tokens.append(token.form)
        
        return tokens
    
    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """
        불용어를 제거합니다.
        
        Args:
            tokens (List[str]): 토큰 리스트
            
        Returns:
            List[str]: 불용어가 제거된 토큰 리스트
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def add_stop_words(self, words: List[str]) -> None:
        """
        불용어 목록에 단어를 추가합니다.
        
        Args:
            words (List[str]): 추가할 단어 리스트
        """
        self.stop_words.update(words)
    
    def remove_stop_words_from_list(self, words: List[str]) -> None:
        """
        불용어 목록에서 단어를 제거합니다.
        
        Args:
            words (List[str]): 제거할 단어 리스트
        """
        self.stop_words.difference_update(words)
