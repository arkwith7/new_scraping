import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from ..config import API_URL
from ..utils.auth import get_auth_header

def dashboard_page():
    st.title("뉴스 분석 대시보드")
    
    # 사이드바 - 뉴스 검색
    with st.sidebar:
        st.header("뉴스 검색")
        keyword = st.text_input("검색어")
        num_results = st.number_input("결과 수", min_value=1, max_value=100, value=10)
        date_range = st.selectbox(
            "기간",
            ["1일", "1주일", "1개월", "3개월", "6개월", "1년"],
            index=1
        )
        sources = st.multiselect(
            "검색 소스",
            ["google", "naver", "sk_hynix", "samsung_semiconductor"],
            default=["google", "naver"]
        )
        
        if st.button("검색"):
            try:
                response = requests.post(
                    f"{API_URL}/news/search",
                    json={
                        "keyword": keyword,
                        "num_results": num_results,
                        "date_range": date_range,
                        "sources": sources
                    },
                    headers=get_auth_header()
                )
                if response.status_code == 200:
                    st.session_state["search_results"] = response.json()["results"]
                    st.success("검색이 완료되었습니다!")
                else:
                    st.error("검색 중 오류가 발생했습니다.")
            except Exception as e:
                st.error(f"검색 중 오류가 발생했습니다: {str(e)}")
    
    # 메인 영역
    if "search_results" in st.session_state:
        results = st.session_state["search_results"]
        
        # 검색 결과 표시
        st.header("검색 결과")
        for news in results:
            with st.expander(f"{news['title']} ({news['source']})"):
                st.write(f"URL: {news['url']}")
                st.write(f"발행일: {news['published_date']}")
                st.write(f"내용: {news['content'][:200]}...")
                
                # 분석 버튼
                if st.button(f"분석하기", key=f"analyze_{news['id']}"):
                    try:
                        response = requests.post(
                            f"{API_URL}/analysis/analyze",
                            json={"news_ids": [news['id']]},
                            headers=get_auth_header()
                        )
                        if response.status_code == 200:
                            st.session_state["analysis_result"] = response.json()
                            st.success("분석이 완료되었습니다!")
                        else:
                            st.error("분석 중 오류가 발생했습니다.")
                    except Exception as e:
                        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        
        # 분석 결과 표시
        if "analysis_result" in st.session_state:
            result = st.session_state["analysis_result"]
            
            st.header("분석 결과")
            
            # 키워드 분석
            st.subheader("키워드 분석")
            keywords_df = pd.DataFrame(
                list(result["keywords"].items()),
                columns=["키워드", "중요도"]
            )
            fig = px.bar(
                keywords_df,
                x="키워드",
                y="중요도",
                title="키워드 중요도"
            )
            st.plotly_chart(fig)
            
            # 감성 분석
            st.subheader("감성 분석")
            sentiment_df = pd.DataFrame(
                list(result["sentiment"].items()),
                columns=["감성", "비율"]
            )
            fig = px.pie(
                sentiment_df,
                values="비율",
                names="감성",
                title="감성 분석 결과"
            )
            st.plotly_chart(fig)
            
            # 토픽 분석
            st.subheader("토픽 분석")
            for topic in result["topics"]:
                st.write(f"토픽 {topic['topic_id'] + 1}")
                st.write(f"주요 키워드: {', '.join(topic['keywords'])}")
                st.write(f"가중치: {topic['weight']:.2f}")
                st.markdown("---") 