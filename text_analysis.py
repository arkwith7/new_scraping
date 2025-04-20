import pandas as pd
from text_preprocessing import TextPreprocessor
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # 데이터 로드
    logger.info("데이터 로드 시작")
    df = pd.read_csv('data/skhynix/leadership_news.csv')
    logger.info(f"데이터 로드 완료: {len(df)} 행")

    # TextPreprocessor 초기화
    logger.info("TextPreprocessor 초기화")
    preprocessor = TextPreprocessor()
    logger.info("TextPreprocessor 초기화 완료")
       
    # 텍스트 전처리 적용
    logger.info("텍스트 전처리 시작")
    df['processed_content'] = df['content'].apply(preprocessor.preprocess_text)
    logger.info("텍스트 전처리 완료")
       
    # 샘플 출력
    print("전처리된 텍스트 샘플:")
    print(df['processed_content'].iloc[0][:200])
       
    # 도메인 키워드 등장 빈도 확인
    logger.info("키워드 빈도 분석 시작")
    keyword_freq = preprocessor.analyze_keywords(df['processed_content'])
    logger.info("키워드 빈도 분석 완료")
       
    print("\n도메인 키워드 등장 빈도:")
    for keyword, freq in sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True):
        print(f"{keyword}: {freq}회")
       
    # N-gram 분석
    logger.info("N-gram 분석 시작")
    ngram_freq = preprocessor.extract_ngrams(df['processed_content'])
    logger.info("N-gram 분석 완료")
       
    print("\n자주 등장하는 N-gram:")
    for ngram, count in list(ngram_freq.items())[:20]:
        print(f"{ngram}: {count}")

except Exception as e:
    logger.error(f"오류 발생: {str(e)}", exc_info=True) 