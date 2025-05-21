import streamlit as st
import json
import requests
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Optional
from ..utils.auth import get_token
from datetime import datetime
import pandas as pd

def visualize_sentiment(sentiment_data: Dict):
    """감성 분석 결과를 시각화합니다."""
    if isinstance(sentiment_data, dict):
        # 감성 점수를 파이 차트로 표시
        labels = list(sentiment_data.keys())
        values = list(sentiment_data.values())
        
        fig = px.pie(
            values=values,
            names=labels,
            title="감성 분석 결과",
            color=labels,
            color_discrete_map={
                "positive": "green",
                "negative": "red",
                "neutral": "gray"
            }
        )
        st.plotly_chart(fig)

def visualize_keywords(keywords_data: Dict):
    """키워드 분석 결과를 시각화합니다."""
    if isinstance(keywords_data, dict) and "keywords" in keywords_data:
        # 키워드 빈도수를 바 차트로 표시
        keywords = []
        frequencies = []
        
        for keyword, freq in keywords_data["keywords"].items():
            keywords.append(keyword)
            frequencies.append(freq)
        
        fig = px.bar(
            x=keywords,
            y=frequencies,
            title="키워드 빈도수",
            labels={"x": "키워드", "y": "빈도수"}
        )
        st.plotly_chart(fig)

def visualize_topics(topics_data: Dict):
    """토픽 분석 결과를 시각화합니다."""
    if isinstance(topics_data, dict) and "topics" in topics_data:
        # 토픽 간의 관계를 네트워크 그래프로 표시
        topics = topics_data["topics"]
        
        # 간단한 바 차트로 토픽 중요도 표시
        topic_names = []
        importance = []
        
        for topic, data in topics.items():
            topic_names.append(topic)
            importance.append(data.get("importance", 0))
        
        fig = px.bar(
            x=topic_names,
            y=importance,
            title="토픽 중요도",
            labels={"x": "토픽", "y": "중요도"}
        )
        st.plotly_chart(fig)

def visualize_comparison(comparison_data: Dict):
    """텍스트 비교 분석 결과를 시각화합니다."""
    if isinstance(comparison_data, dict):
        # 유사도 점수를 레이더 차트로 표시
        if "similarity_scores" in comparison_data:
            categories = list(comparison_data["similarity_scores"].keys())
            values = list(comparison_data["similarity_scores"].values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='유사도'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                title="텍스트 유사도 분석"
            )
            st.plotly_chart(fig)

def analyze_text(text: str, analysis_type: str) -> Dict:
    """텍스트 분석 API를 호출합니다."""
    token = get_token()
    if not token:
        st.error("로그인이 필요합니다.")
        return None
    
    try:
        response = requests.post(
            f"{st.session_state.api_url}/analysis/analyze",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": text, "analysis_type": analysis_type}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        return None

def compare_texts(text1: str, text2: str) -> Dict:
    """텍스트 비교 분석 API를 호출합니다."""
    token = get_token()
    if not token:
        st.error("로그인이 필요합니다.")
        return None
    
    try:
        response = requests.post(
            f"{st.session_state.api_url}/analysis/compare",
            headers={"Authorization": f"Bearer {token}"},
            json={"text1": text1, "text2": text2}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"비교 분석 중 오류가 발생했습니다: {str(e)}")
        return None

def summarize_text(text: str, max_length: Optional[int] = None) -> Dict:
    """텍스트 요약 API를 호출합니다."""
    token = get_token()
    if not token:
        st.error("로그인이 필요합니다.")
        return None
    
    try:
        response = requests.post(
            f"{st.session_state.api_url}/analysis/summarize",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": text, "max_length": max_length}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"요약 중 오류가 발생했습니다: {str(e)}")
        return None

def show_history():
    st.header("분석 히스토리")
    
    history_type = st.selectbox(
        "히스토리 유형",
        ["analysis", "comparison", "summary"]
    )
    
    try:
        response = requests.get(
            f"{st.session_state.api_url}/analysis/history/{history_type}",
            headers={"Authorization": f"Bearer {get_token()}"}
        )
        response.raise_for_status()
        history = response.json()
        
        if not history:
            st.info("히스토리가 없습니다.")
            return
            
        for item in history:
            with st.expander(f"{item['analysis_type'] if history_type == 'analysis' else '비교' if history_type == 'comparison' else '요약'} - {datetime.fromisoformat(item['created_at']).strftime('%Y-%m-%d %H:%M:%S')}"):
                if history_type == "analysis":
                    st.write("분석 텍스트:")
                    st.text(item["text"])
                    st.write("분석 결과:")
                    st.json(item["result"])
                elif history_type == "comparison":
                    st.write("텍스트 1:")
                    st.text(item["text1"])
                    st.write("텍스트 2:")
                    st.text(item["text2"])
                    st.write("비교 결과:")
                    st.json(item["result"])
                else:  # summary
                    st.write("원본 텍스트:")
                    st.text(item["text"])
                    st.write("요약 결과:")
                    st.text(item["result"]["summary"])
                    
    except Exception as e:
        st.error(f"히스토리 조회 중 오류가 발생했습니다: {str(e)}")

def render():
    st.title("AI 텍스트 분석")
    
    # 분석 유형 선택
    analysis_type = st.selectbox(
        "분석 유형",
        ["comprehensive", "sentiment", "keywords", "topics"],
        format_func=lambda x: {
            "comprehensive": "종합 분석",
            "sentiment": "감성 분석",
            "keywords": "키워드 분석",
            "topics": "토픽 분석"
        }[x]
    )
    
    # 텍스트 입력
    text = st.text_area("분석할 텍스트를 입력하세요", height=200)
    
    if st.button("분석"):
        if text:
            with st.spinner("분석 중..."):
                result = analyze_text(text, analysis_type)
                if result:
                    # 분석 결과 시각화
                    if analysis_type == "sentiment":
                        visualize_sentiment(result)
                    elif analysis_type == "keywords":
                        visualize_keywords(result)
                    elif analysis_type == "topics":
                        visualize_topics(result)
                    elif analysis_type == "comprehensive":
                        if "sentiment" in result:
                            visualize_sentiment(result["sentiment"])
                        if "keywords" in result:
                            visualize_keywords(result["keywords"])
                        if "topics" in result:
                            visualize_topics(result["topics"])
                    
                    # 상세 결과 표시
                    st.subheader("상세 분석 결과")
                    st.json(result)
        else:
            st.warning("텍스트를 입력해주세요.")
    
    st.markdown("---")
    
    # 텍스트 비교 분석
    st.subheader("텍스트 비교 분석")
    col1, col2 = st.columns(2)
    
    with col1:
        text1 = st.text_area("첫 번째 텍스트", height=150)
    
    with col2:
        text2 = st.text_area("두 번째 텍스트", height=150)
    
    if st.button("비교 분석"):
        if text1 and text2:
            with st.spinner("비교 분석 중..."):
                result = compare_texts(text1, text2)
                if result:
                    # 비교 결과 시각화
                    visualize_comparison(result)
                    
                    # 상세 결과 표시
                    st.subheader("상세 비교 결과")
                    st.json(result)
        else:
            st.warning("두 텍스트를 모두 입력해주세요.")
    
    st.markdown("---")
    
    # 텍스트 요약
    st.subheader("텍스트 요약")
    summary_text = st.text_area("요약할 텍스트를 입력하세요", height=200)
    max_length = st.number_input("최대 요약 길이 (선택사항)", min_value=0, value=0)
    
    if st.button("요약"):
        if summary_text:
            with st.spinner("요약 중..."):
                result = summarize_text(summary_text, max_length if max_length > 0 else None)
                if result:
                    # 요약 결과 표시
                    st.subheader("요약 결과")
                    st.write(result["summary"])
                    
                    # 원본과 요약의 길이 비교
                    fig = go.Figure(data=[
                        go.Bar(
                            x=["원본", "요약"],
                            y=[result["original_length"], result["summary_length"]],
                            text=[result["original_length"], result["summary_length"]],
                            textposition='auto',
                        )
                    ])
                    fig.update_layout(title="텍스트 길이 비교")
                    st.plotly_chart(fig)
                    
                    # 상세 정보 표시
                    st.json(result)
        else:
            st.warning("텍스트를 입력해주세요.")
    
    st.markdown("---")
    
    # 분석 히스토리
    show_history()

if __name__ == "__main__":
    render() 