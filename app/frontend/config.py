import os

# API URL 설정
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

# 페이지 설정
PAGES = {
    "로그인": "login",
    "회원가입": "register",
    "대시보드": "dashboard"
}

# 스타일 설정
STYLE = """
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stExpander {
        margin-bottom: 1rem;
    }
</style>
""" 