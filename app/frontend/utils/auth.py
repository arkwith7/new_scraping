import streamlit as st

def get_auth_header():
    """
    인증 헤더를 반환합니다.
    """
    if "token" not in st.session_state:
        st.error("로그인이 필요합니다.")
        st.stop()
    
    return {"Authorization": f"Bearer {st.session_state['token']}"}

def check_auth():
    """
    인증 상태를 확인합니다.
    """
    if "token" not in st.session_state:
        st.warning("로그인이 필요합니다.")
        st.markdown("[로그인](/login) 페이지로 이동하세요.")
        st.stop()

def logout():
    """
    로그아웃을 수행합니다.
    """
    if "token" in st.session_state:
        del st.session_state["token"]
    st.experimental_rerun() 