from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes import search
from .newsroom import router as newsroom_router

app = FastAPI(
    title="뉴스 스크래핑 및 텍스트 분석 API",
    description="구글과 네이버 검색 API를 활용한 뉴스 텍스트 수집 및 분석 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(search.router, prefix="/api/v1", tags=["search"])

router = APIRouter()
router.include_router(newsroom_router, prefix="/api/v1", tags=["newsroom"])

@app.get("/")
async def root():
    return {"message": "뉴스 스크래핑 및 텍스트 분석 API 서버가 실행 중입니다."}
