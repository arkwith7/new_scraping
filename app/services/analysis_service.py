from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..db.models import NewsData, AnalysisResult
from ..schemas.analysis import AnalysisCreate, AnalysisResult as AnalysisResultSchema
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob

class NewsAnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.okt = Okt()
    
    def analyze_news(self, news_list: List[NewsData]) -> AnalysisResult:
        # 텍스트 전처리
        texts = [news.content for news in news_list]
        processed_texts = [self._preprocess_text(text) for text in texts]
        
        # 키워드 추출
        keywords = self._extract_keywords(processed_texts)
        
        # 감성 분석
        sentiment = self._analyze_sentiment(processed_texts)
        
        # 토픽 모델링
        topics = self._extract_topics(processed_texts)
        
        # 분석 결과 저장
        analysis_result = AnalysisResult(
            news_ids=[news.id for news in news_list],
            keywords=keywords,
            sentiment=sentiment,
            topics=topics,
            created_at=datetime.utcnow()
        )
        self.db.add(analysis_result)
        self.db.commit()
        self.db.refresh(analysis_result)
        
        return analysis_result
    
    def _preprocess_text(self, text: str) -> str:
        # 한글 형태소 분석
        pos_tagged = self.okt.pos(text)
        # 명사, 동사, 형용사만 추출
        words = [word for word, pos in pos_tagged if pos in ['Noun', 'Verb', 'Adjective']]
        return ' '.join(words)
    
    def _extract_keywords(self, texts: List[str]) -> Dict[str, float]:
        # TF-IDF 벡터화
        vectorizer = TfidfVectorizer(max_features=20)
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # 키워드와 TF-IDF 점수 추출
        feature_names = vectorizer.get_feature_names_out()
        scores = np.mean(tfidf_matrix.toarray(), axis=0)
        
        return dict(zip(feature_names, scores))
    
    def _analyze_sentiment(self, texts: List[str]) -> Dict[str, float]:
        sentiments = []
        for text in texts:
            blob = TextBlob(text)
            sentiments.append(blob.sentiment.polarity)
        
        return {
            'positive': len([s for s in sentiments if s > 0]) / len(sentiments),
            'neutral': len([s for s in sentiments if s == 0]) / len(sentiments),
            'negative': len([s for s in sentiments if s < 0]) / len(sentiments)
        }
    
    def _extract_topics(self, texts: List[str], n_topics: int = 3) -> List[Dict[str, Any]]:
        # TF-IDF 벡터화
        vectorizer = TfidfVectorizer(max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # LDA 모델 학습
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            max_iter=10,
            learning_method='online',
            random_state=42
        )
        lda.fit(tfidf_matrix)
        
        # 토픽별 키워드 추출
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-10-1:-1]]
            topics.append({
                'topic_id': topic_idx,
                'keywords': top_words,
                'weight': float(np.mean(topic))
            })
        
        return topics
    
    def get_analysis_result(self, analysis_id: int) -> AnalysisResult:
        return self.db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    
    def get_user_analysis_results(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AnalysisResult]:
        return self.db.query(AnalysisResult)\
            .filter(AnalysisResult.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all() 