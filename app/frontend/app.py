import streamlit as st
from .config import STYLE, PAGES
from .pages import login, register, dashboard
from .utils.auth import check_auth

def main():
    # 스타일 적용
    st.markdown(STYLE, unsafe_allow_html=True)
    
    # 사이드바 - 네비게이션
    st.sidebar.title("뉴스 분석 서비스")
    
    # 로그인 상태에 따른 네비게이션
    if "token" in st.session_state:
        st.sidebar.success("로그인됨")
        if st.sidebar.button("로그아웃"):
            from .utils.auth import logout
            logout()
    
    # 페이지 선택
    page = st.sidebar.radio("페이지", list(PAGES.keys()))
    
    # 페이지 라우팅
    if page == "로그인":
        login.login_page()
    elif page == "회원가입":
        register.register_page()
    elif page == "대시보드":
        check_auth()
        dashboard.dashboard_page()

if __name__ == "__main__":
    main() 