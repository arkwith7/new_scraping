import pandas as pd
import numpy as np
from konlpy.tag import Mecab
import re
from collections import Counter
from nltk import bigrams
import nltk
from sklearn.feature_extraction.text import CountVectorizer

# 도메인 키워드 정의
domain_keywords = {
    '탐색적 리더십(Exploration)': [
        '탐색', 'Exploration', 'CEO', '사장', '대표이사', '회장', '경영진', '임원', '수석', '총괄', 
        '책임자', '이사', '혁신', '변화', '연구', '투자', '실패 수용', '장기적 이익', '대담한 전략', 
        '혁신적 사고', '조직 변화', '비전', '권한 위임', '적응력', '유연성', '위기 관리', '변혁적 리더십', 
        '개발', '진정성 리더십', '지속가능성'
    ],
    '활용적 리더십(Exploitation)': [
        '활용', 'Exploitation', 'CEO', '사장', '대표이사', '회장', '경영진', '임원', '수석', '총괄', 
        '책임자', '이사', '성과', '성장', '경영', '전략', '위험 회피', '단기적 이익', '효율적 운영', 
        '지속적 개선', '인재 개발', '의사결정', '동기 부여', '팀워크', '소통', '성과 관리', '문제 해결', 
        '조직 문화', '고객 중심', '관계 구축', '협업', '영향력', '윤리적 리더십', '섬김의 리더십'
    ],
    'semiconductor': [
        'HBM', 'HBM1', 'HBM2', 'HBM2E', 'HBM3', 'HBM3E', 'HBM4',
        'DDR4', 'DDR5', 'DDR6', 'LPDDR6',
        'DRAM', 'D램', 'NAND', '낸드', '플래시',
        'TSV', 'Through Silicon Via',
        '1αnm', '1-alpha', '1γnm', '1-gamma', '1δnm', '1-delta',
        'VG DRAM', 'Vertical Gate', '3D DRAM',
        '파운드리', '팹리스', '패키징', '웨이퍼'
    ],
    'companies': [
        'SK하이닉스', 'SK hynix', '삼성전자', 'TSMC', '인텔', '마이크론',
        '퀄컴', 'AMD', '엔비디아', '아마존', '구글', '애플'
    ],
    'technology': [
        'AI', '인공지능', '빅데이터', '클라우드', '5G', '6G', 'IoT',
        '자율주행', '메타버스', '양자컴퓨팅', '로봇', '자동화',
        '스마트팩토리', '디지털트랜스포메이션'
    ]
}

# 모든 도메인 키워드를 하나의 리스트로 통합
all_domain_keywords = [keyword for keywords in domain_keywords.values() for keyword in keywords]

class TextPreprocessor:
    def __init__(self, custom_dict_path=None):
        """
        텍스트 전처리기 초기화
        Args:
            custom_dict_path (str): 사용자 사전 파일 경로
        """
        # 사용자 사전 생성
        self._create_custom_dict()
        
        # Mecab 초기화 (사용자 사전 적용)
        self.mecab = Mecab(dicpath='/usr/local/lib/mecab/dic/mecab-ko-dic')
        # self.smecab = Mecab(dicpath='/usr/local/lib/mecab/dic/mecab-ko-dic', userdic='custom_dict.csv')
        
        # NLTK 초기화
        nltk.download('punkt', quiet=True)
        
        # 영어 키워드 패턴 컴파일
        self.english_pattern = re.compile(r'\b[A-Za-z]+[0-9]*[A-Za-z]*[0-9]*\b')
        
        # 영어-한글 혼합 패턴 컴파일
        self.mixed_pattern = re.compile(r'[A-Za-z]+[가-힣]+|[가-힣]+[A-Za-z]+')
        
        # CountVectorizer 초기화 (N-gram 추출용)
        self.vectorizer = CountVectorizer(
            ngram_range=(1, 2),
            token_pattern=r'[가-힣A-Za-z0-9]+',
            min_df=2
        )
    
    def _create_custom_dict(self):
        """사용자 사전 생성"""
        custom_dict = []
        for keyword in all_domain_keywords:
            if ' ' in keyword:  # 복합어인 경우
                custom_dict.append(f"{keyword},*,*,*,*,*,*,*,*,*,*,*,*,*")
            else:  # 단일어인 경우
                custom_dict.append(f"{keyword},*,*,*,*,*,*,*,*,*,*,*,*,*")
        
        # 사용자 사전 저장
        with open('custom_dict.csv', 'w', encoding='utf-8') as f:
            f.write('\n'.join(custom_dict))
    
    def extract_english_terms(self, text):
        """영어 키워드 추출"""
        # 영어 단어 추출
        english_terms = set(self.english_pattern.findall(text))
        
        # 영어-한글 혼합어 추출
        mixed_terms = set(self.mixed_pattern.findall(text))
        
        return english_terms.union(mixed_terms)
    
    def preprocess_text(self, text):
        """
        텍스트 전처리
        Args:
            text (str): 전처리할 텍스트
        Returns:
            str: 전처리된 텍스트
        """
        if pd.isna(text):
            return ''
        
        # 1. 영어 키워드 추출 및 보존
        english_terms = self.extract_english_terms(text)
        for term in english_terms:
            text = text.replace(term, f" {term} ")
        
        # 2. 도메인 키워드 보존
        for keyword in all_domain_keywords:
            text = text.replace(keyword, f" {keyword} ")
        
        # 3. 특수문자 제거
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 4. 형태소 분석
        pos = self.mecab.pos(text)
        
        # 5. 의미 있는 단어 추출
        words = []
        for word, pos_tag in pos:
            # 영어 키워드는 보존
            if word in english_terms:
                words.append(word)
                continue
            
            # 도메인 키워드는 보존
            if word in all_domain_keywords:
                words.append(word)
                continue
            
            # 일반 명사, 형용사, 동사 추출
            if pos_tag in ['NNG', 'NNP', 'VA', 'VV']:
                if not (len(word) == 1 and '\u4e00' <= word <= '\u9fff'):
                    words.append(word)
        
        return ' '.join(words)
    
    def extract_ngrams(self, texts, n_range=(2, 3)):
        """
        N-gram 추출 및 빈도 분석
        Args:
            texts (list): 텍스트 리스트
            n_range (tuple): N-gram 범위 (최소, 최대)
        Returns:
            dict: N-gram 빈도
        """
        # CountVectorizer로 N-gram 추출
        ngram_matrix = self.vectorizer.fit_transform(texts)
        
        # N-gram 빈도 계산
        ngram_freq = ngram_matrix.sum(axis=0).A1
        ngram_features = self.vectorizer.get_feature_names_out()
        
        # 빈도순 정렬
        ngram_dict = dict(zip(ngram_features, ngram_freq))
        return dict(sorted(ngram_dict.items(), key=lambda x: x[1], reverse=True))
    
    def analyze_keywords(self, texts):
        """
        키워드 빈도 분석
        Args:
            texts (list): 텍스트 리스트
        Returns:
            dict: 키워드 빈도
        """
        keyword_freq = {}
        for keyword in all_domain_keywords:
            freq = sum(1 for text in texts if keyword in text)
            if freq > 0:
                keyword_freq[keyword] = freq
        return keyword_freq
    
    def process_dataframe(self, df, text_column='content'):
        """
        데이터프레임 전체 처리
        Args:
            df (DataFrame): 처리할 데이터프레임
            text_column (str): 텍스트 컬럼명
        Returns:
            DataFrame: 처리된 데이터프레임
        """
        df['processed_content'] = df[text_column].apply(self.preprocess_text)
        return df 