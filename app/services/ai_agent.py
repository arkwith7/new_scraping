from typing import Dict, List, Optional
import openai
from app.core.config import settings

class TextAnalysisAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
    async def analyze_text(self, text: str, analysis_type: str = "comprehensive") -> Dict:
        """
        텍스트를 분석하여 다양한 인사이트를 제공합니다.
        
        Args:
            text: 분석할 텍스트
            analysis_type: 분석 유형 (comprehensive, sentiment, keywords, topics)
            
        Returns:
            Dict: 분석 결과
        """
        prompt = self._create_prompt(text, analysis_type)
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 텍스트 분석가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"텍스트 분석 중 오류가 발생했습니다: {str(e)}")
    
    def _create_prompt(self, text: str, analysis_type: str) -> str:
        """분석 유형에 따른 프롬프트를 생성합니다."""
        base_prompt = f"다음 텍스트를 분석해주세요:\n\n{text}\n\n"
        
        prompts = {
            "comprehensive": base_prompt + """
            다음 항목들을 분석해주세요:
            1. 주요 키워드와 핵심 개념
            2. 텍스트의 감성 (긍정/부정/중립)
            3. 주요 토픽과 주제
            4. 텍스트의 신뢰성과 객관성
            5. 핵심 메시지와 결론
            
            JSON 형식으로 응답해주세요.
            """,
            
            "sentiment": base_prompt + """
            텍스트의 감성을 분석해주세요:
            1. 전체적인 감성 (긍정/부정/중립)
            2. 감성의 강도 (0-1 사이의 값)
            3. 주요 감성 표현
            4. 감성 변화 추이
            
            JSON 형식으로 응답해주세요.
            """,
            
            "keywords": base_prompt + """
            텍스트에서 다음을 추출해주세요:
            1. 주요 키워드 (빈도수 포함)
            2. 핵심 개념
            3. 중요 문구
            4. 키워드 간의 관계
            
            JSON 형식으로 응답해주세요.
            """,
            
            "topics": base_prompt + """
            텍스트의 주제를 분석해주세요:
            1. 주요 토픽
            2. 토픽 간의 관계
            3. 각 토픽의 중요도
            4. 토픽의 발전 방향
            
            JSON 형식으로 응답해주세요.
            """
        }
        
        return prompts.get(analysis_type, prompts["comprehensive"])
    
    def _parse_response(self, response: str) -> Dict:
        """ChatGPT의 응답을 파싱하여 구조화된 데이터로 변환합니다."""
        try:
            # JSON 형식의 응답을 파싱
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트를 구조화
            return {
                "raw_analysis": response,
                "error": "응답을 JSON으로 파싱할 수 없습니다."
            }
    
    async def compare_texts(self, text1: str, text2: str) -> Dict:
        """
        두 텍스트를 비교 분석합니다.
        
        Args:
            text1: 첫 번째 텍스트
            text2: 두 번째 텍스트
            
        Returns:
            Dict: 비교 분석 결과
        """
        prompt = f"""
        다음 두 텍스트를 비교 분석해주세요:
        
        텍스트 1:
        {text1}
        
        텍스트 2:
        {text2}
        
        다음 항목들을 비교해주세요:
        1. 주요 키워드와 개념의 유사성
        2. 감성의 차이
        3. 주제와 토픽의 차이
        4. 정보의 일관성
        5. 전체적인 유사도
        
        JSON 형식으로 응답해주세요.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 텍스트 비교 분석가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"텍스트 비교 분석 중 오류가 발생했습니다: {str(e)}")
    
    async def summarize_text(self, text: str, max_length: Optional[int] = None) -> Dict:
        """
        텍스트를 요약합니다.
        
        Args:
            text: 요약할 텍스트
            max_length: 최대 요약 길이 (선택사항)
            
        Returns:
            Dict: 요약 결과
        """
        prompt = f"""
        다음 텍스트를 요약해주세요:
        
        {text}
        
        요약 시 다음 사항을 고려해주세요:
        1. 핵심 메시지와 주요 내용
        2. 중요한 세부 사항
        3. 결론과 시사점
        """
        
        if max_length:
            prompt += f"\n\n요약의 최대 길이는 {max_length}자입니다."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 텍스트 요약가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                "summary": response.choices[0].message.content,
                "original_length": len(text),
                "summary_length": len(response.choices[0].message.content)
            }
            
        except Exception as e:
            raise Exception(f"텍스트 요약 중 오류가 발생했습니다: {str(e)}") 