import streamlit as st
import requests
from ..config import API_URL

def register_page():
    st.title("회원가입")
    
    with st.form("register_form"):
        email = st.text_input("이메일")
        full_name = st.text_input("이름")
        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")
        submit = st.form_submit_button("회원가입")
        
        if submit:
            if password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다.")
                return
            
            try:
                response = requests.post(
                    f"{API_URL}/register",
                    json={
                        "email": email,
                        "full_name": full_name,
                        "password": password
                    }
                )
                if response.status_code == 200:
                    st.success("회원가입이 완료되었습니다!")
                    st.markdown("로그인 페이지로 이동하세요: [로그인](/login)")
                else:
                    st.error("회원가입 중 오류가 발생했습니다.")
            except Exception as e:
                st.error(f"회원가입 중 오류가 발생했습니다: {str(e)}")
    
    st.markdown("---")
    st.markdown("이미 계정이 있으신가요? [로그인](/login) 페이지로 이동하세요.") 