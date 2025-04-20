from konlpy.tag import Mecab
import os

# 현재 작업 디렉토리에서 사용자 정의 사전 파일 경로 설정
custom_dict_path = 'custom_dict.csv'

# Mecab 초기화
mecab = Mecab(dicpath='/usr/local/lib/mecab/dic/mecab-ko-dic')

# 테스트 텍스트
text = 'AI리더십과 DDR5 메모리 기술'

# 형태소 분석
result = mecab.morphs(text)
print("형태소 분석 결과:", result)

# 품사 태그와 함께 출력
pos_result = mecab.pos(text)
print("\n품사 태그 분석 결과:", pos_result) 