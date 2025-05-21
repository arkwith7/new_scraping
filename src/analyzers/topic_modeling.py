from typing import List, Dict, Tuple
import numpy as np
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
from ..utils.text_preprocessing import TextPreprocessor
from kiwipiepy import Kiwi

class TopicModeler:
    """토픽 모델링을 수행하는 클래스"""
    
    def __init__(self):
        self.kiwi = Kiwi()
        self.preprocessor = TextPreprocessor()
        self.dictionary = None
        self.corpus = None
        self.model = None
    
    def prepare_corpus(self, texts: List[str]) -> None:
        """
        코퍼스를 준비합니다.
        
        Args:
            texts (List[str]): 분석할 텍스트 리스트
        """
        # 텍스트 전처리
        processed_texts = [self.preprocessor.preprocess(text) for text in texts]
        
        # 형태소 분석
        tokenized_texts = []
        for text in processed_texts:
            result = self.kiwi.analyze(text)
            tokens = [token.form for token in result[0][0]]
            tokenized_texts.append(tokens)
        
        # 사전 생성
        self.dictionary = corpora.Dictionary(tokenized_texts)
        
        # 코퍼스 생성
        self.corpus = [self.dictionary.doc2bow(text) for text in tokenized_texts]
    
    def train_model(self, num_topics: int = 5, passes: int = 10) -> None:
        """
        LDA 모델을 학습합니다.
        
        Args:
            num_topics (int): 토픽 수
            passes (int): 학습 반복 횟수
        """
        if self.corpus is None or self.dictionary is None:
            raise ValueError("코퍼스를 먼저 준비해야 합니다.")
        
        self.model = models.LdaModel(
            corpus=self.corpus,
            id2word=self.dictionary,
            num_topics=num_topics,
            passes=passes,
            random_state=42
        )
    
    def get_topics(self, num_words: int = 10) -> List[Dict]:
        """
        학습된 토픽을 반환합니다.
        
        Args:
            num_words (int): 토픽당 단어 수
            
        Returns:
            List[Dict]: 토픽 리스트
        """
        if self.model is None:
            raise ValueError("모델을 먼저 학습해야 합니다.")
        
        topics = []
        for topic_id in range(self.model.num_topics):
            topic_words = self.model.show_topic(topic_id, num_words)
            topics.append({
                'topic_id': topic_id,
                'words': [{'word': word, 'probability': prob} for word, prob in topic_words]
            })
        
        return topics
    
    def get_document_topics(self, text: str) -> List[Dict]:
        """
        문서의 토픽 분포를 반환합니다.
        
        Args:
            text (str): 분석할 텍스트
            
        Returns:
            List[Dict]: 토픽 분포 리스트
        """
        if self.model is None:
            raise ValueError("모델을 먼저 학습해야 합니다.")
        
        # 텍스트 전처리 및 토큰화
        processed_text = self.preprocessor.preprocess(text)
        result = self.kiwi.analyze(processed_text)
        tokens = [token.form for token in result[0][0]]
        
        # 문서 벡터 생성
        doc_bow = self.dictionary.doc2bow(tokens)
        
        # 토픽 분포 계산
        topic_dist = self.model.get_document_topics(doc_bow)
        
        return [{'topic_id': topic_id, 'probability': prob} for topic_id, prob in topic_dist]
    
    def evaluate_model(self) -> Dict:
        """
        모델의 성능을 평가합니다.
        
        Returns:
            Dict: 평가 결과
        """
        if self.model is None:
            raise ValueError("모델을 먼저 학습해야 합니다.")
        
        # Perplexity 계산
        perplexity = self.model.log_perplexity(self.corpus)
        
        # Coherence 계산
        coherence_model = CoherenceModel(
            model=self.model,
            texts=[[self.dictionary[word_id] for word_id, _ in doc] for doc in self.corpus],
            dictionary=self.dictionary,
            coherence='c_v'
        )
        coherence = coherence_model.get_coherence()
        
        return {
            'perplexity': perplexity,
            'coherence': coherence
        }
