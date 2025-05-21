import streamlit as st
import requests
from ..config import API_URL

def login_page():
    st.title("로그인")
    
    with st.form("login_form"):
        email = st.text_input("이메일")
        password = st.text_input("비밀번호", type="password")
        submit = st.form_submit_button("로그인")
        
        if submit:
            try:
                response = requests.post(
                    f"{API_URL}/login",
                    data={"username": email, "password": password}
                )
                if response.status_code == 200:
                    token = response.json()["access_token"]
                    st.session_state["token"] = token
                    st.success("로그인 성공!")
                    st.experimental_rerun()
                else:
                    st.error("이메일 또는 비밀번호가 올바르지 않습니다.")
            except Exception as e:
                st.error(f"로그인 중 오류가 발생했습니다: {str(e)}")
    
    st.markdown("---")
    st.markdown("계정이 없으신가요? [회원가입](/register) 페이지로 이동하세요.") 