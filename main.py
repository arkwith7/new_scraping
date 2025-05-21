from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import news, users, analysis
from app.db.session import engine
from app.db.models import Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(news.router, prefix=settings.API_V1_STR, tags=["news"])
app.include_router(analysis.router, prefix=settings.API_V1_STR, tags=["analysis"])

@app.get("/")
async def root():
    return {
        "message": "뉴스 분석 서비스 API",
        "version": settings.VERSION
    } 