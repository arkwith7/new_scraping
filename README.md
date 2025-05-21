# 뉴스 분석 서비스

뉴스 데이터를 수집하고 분석하는 서비스입니다. FastAPI 백엔드와 Streamlit 프론트엔드로 구성되어 있으며, OpenAI API를 활용한 텍스트 분석 기능을 제공합니다.

## 주요 기능

### 1. 뉴스 수집
- Google News API를 통한 뉴스 수집
- 네이버 뉴스 크롤링
- SK하이닉스 뉴스 크롤링
- 삼성반도체 뉴스 크롤링
- 사용자별 뉴스 저장 및 관리

### 2. 뉴스 분석
- 키워드 추출 및 중요도 분석
- 감성 분석 (긍정/부정/중립)
- 토픽 모델링 및 분류
- 텍스트 비교 분석
- 텍스트 요약 (원문 대비 30-50% 축약)

### 3. 사용자 관리
- 회원가입/로그인 (JWT 기반)
- 사용자별 API 사용량 추적
- 요금제 관리 (무료/프리미엄)
- LLM 토큰 사용량 관리
  - 총 토큰 사용량 추적
  - 월간 토큰 사용량 제한
  - 작업 유형별 토큰 사용량 분석
  - 토큰 사용량 통계 및 리포트

### 4. 데이터 시각화
- 감성 분석 결과 파이 차트
- 키워드 중요도 막대 그래프
- 토픽 관련도 시각화
- 텍스트 비교 레이더 차트
- 토큰 사용량 추이 그래프

### 5. 분석 히스토리
- 분석 결과 저장 및 조회
- 비교 분석 히스토리
- 요약 히스토리
- 상세 분석 정보 확인
- 토큰 사용량 기록 조회

## 기술 스택

### 백엔드
- FastAPI: 고성능 비동기 웹 프레임워크
- SQLAlchemy: ORM 및 데이터베이스 관리
- PostgreSQL: 관계형 데이터베이스
- OpenAI API: 텍스트 분석 및 생성
- Google News API: 뉴스 데이터 수집
- BeautifulSoup4: 웹 크롤링
- JWT: 사용자 인증

### 프론트엔드
- Streamlit: 데이터 시각화 및 웹 인터페이스
- Plotly: 인터랙티브 차트
- Pandas: 데이터 처리 및 분석

### 인프라
- Docker: 컨테이너화
- Nginx: 리버스 프록시 및 SSL 종단점
- PostgreSQL: 데이터베이스

## 프로젝트 구조
```
news_scraping/
├── alembic/              # 데이터베이스 마이그레이션
│   ├── versions/        # 마이그레이션 스크립트
│   └── env.py          # 마이그레이션 환경 설정
├── app/
│   ├── api/            # API 엔드포인트
│   │   ├── routes/    # API 라우트
│   │   └── deps.py    # 의존성 주입
│   ├── core/          # 핵심 설정
│   │   ├── config.py  # 환경 설정
│   │   └── security.py # 보안 설정
│   ├── db/            # 데이터베이스
│   │   ├── models.py  # SQLAlchemy 모델
│   │   └── session.py # DB 세션
│   ├── frontend/      # Streamlit 프론트엔드
│   │   ├── app.py    # 메인 앱
│   │   └── pages/    # 페이지 컴포넌트
│   ├── services/      # 비즈니스 로직
│   │   ├── news.py   # 뉴스 서비스
│   │   ├── analysis.py # 분석 서비스
│   │   └── user.py   # 사용자 서비스
│   └── schemas/       # Pydantic 모델
├── nginx/             # Nginx 설정
│   ├── nginx.conf    # Nginx 설정
│   ├── ssl/          # SSL 인증서
│   └── logs/         # Nginx 로그
├── scripts/          # 유틸리티 스크립트
│   ├── deploy.sh    # 배포 스크립트
│   └── migrate.sh   # 마이그레이션 스크립트
├── tests/           # 테스트 코드
├── .env            # 환경 변수
├── docker-compose.yml # Docker 설정
└── requirements.txt  # 의존성 목록
```

## 설치 및 실행

### 1. 환경 설정
```bash
# Python 3.8 이상 설치
sudo apt update
sudo apt install python3.8 python3.8-venv

# 가상환경 생성 및 활성화
python3.8 -m venv venv
source venv/bin/activate

# 필요한 환경 변수 설정
export OPENAI_API_KEY=your_api_key
export GOOGLE_NEWS_API_KEY=your_api_key
export SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost/news_analysis
export API_URL=http://localhost:8000/api/v1
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 설정
```bash
# PostgreSQL 설치
sudo apt install postgresql postgresql-contrib

# 데이터베이스 생성
sudo -u postgres createdb news_analysis

# 마이그레이션 실행
./scripts/migrate.sh upgrade
```

### 4. 서비스 실행
```bash
# 백엔드 서버 실행
uvicorn app.main:app --reload

# 프론트엔드 실행
streamlit run app/frontend/app.py
```

## 배포 가이드

### 1. 클라우드 서비스 선택

#### AWS 배포 (t3.small)
- CPU: 2 vCPU
- 메모리: 2GB
- 스토리지: 30GB
- 월 예상 비용: $20-25
- 추천 사용자 수: 100명 이하

#### Azure 배포 (Standard_B2s)
- CPU: 2 vCPU
- 메모리: 4GB
- 스토리지: 30GB
- 월 예상 비용: $25-30
- 추천 사용자 수: 100명 이하

### 2. 서버 설정
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. 프로젝트 배포
```bash
# 프로젝트 클론
git clone https://github.com/your-username/news_scraping.git
cd news_scraping

# 환경 변수 설정
export DOMAIN=your-domain.com
export OPENAI_API_KEY=your_api_key
export GOOGLE_NEWS_API_KEY=your_api_key

# 배포 스크립트 실행
./scripts/deploy.sh
```

### 4. 모니터링
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 리소스 사용량 확인
docker stats
```

### 5. 백업
```bash
# 데이터베이스 백업
docker-compose exec postgres pg_dump -U postgres news_analysis > backup.sql

# 데이터베이스 복원
cat backup.sql | docker-compose exec -T postgres psql -U postgres news_analysis
```

## API 엔드포인트

### 인증
- POST /api/v1/auth/register: 회원가입
- POST /api/v1/auth/login: 로그인
- GET /api/v1/auth/me: 현재 사용자 정보

### 뉴스
- GET /api/v1/news/search: 뉴스 검색
- GET /api/v1/news/{news_id}: 특정 뉴스 조회
- GET /api/v1/news/user: 사용자별 뉴스 조회

### 분석
- POST /api/v1/analysis/analyze: 텍스트 분석
- POST /api/v1/analysis/compare: 텍스트 비교
- POST /api/v1/analysis/summarize: 텍스트 요약
- GET /api/v1/analysis/history/analysis: 분석 히스토리
- GET /api/v1/analysis/history/comparison: 비교 히스토리
- GET /api/v1/analysis/history/summary: 요약 히스토리

### 토큰 사용량
- GET /api/v1/users/me/token-usage: 토큰 사용량 기록 조회
- GET /api/v1/users/me/token-stats: 토큰 사용량 통계 조회

## 요금제 및 제한사항

### 무료 요금제
- 월간 토큰 사용량: 10만 토큰
- 기본 분석 기능 사용 가능
- 기본 시각화 기능 사용 가능
- API 호출 제한: 분당 10회

### 프리미엄 요금제
- 월간 토큰 사용량: 100만 토큰
- 모든 분석 기능 사용 가능
- 고급 시각화 기능 사용 가능
- API 호출 제한: 분당 50회
- 우선 지원

## 스케일링 가이드라인

### 사용자 증가에 따른 스케일링
1. 100명 이하: 단일 서버 구성
2. 100-500명: 서버 스케일 업 (t3.medium / Standard_D2s_v3)
3. 500명 이상: 서비스 분리 및 로드 밸런서 추가

### 데이터 증가에 따른 스케일링
1. 20GB 이하: 단일 서버 구성
2. 20-100GB: 스토리지 확장
3. 100GB 이상: 데이터베이스 분리 고려

## 라이선스
MIT License

## 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 환경 변수들을 설정합니다:

### 필수 환경 변수
```bash
# 애플리케이션 설정
APP_NAME=news_scraping
APP_ENV=development  # development, production, testing
API_VERSION=v1
API_PREFIX=/api/v1

# 데이터베이스 설정
DB_DRIVER=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=news_analysis
DB_USER=postgres
DB_PASSWORD=postgres
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost/news_analysis

# JWT 설정
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API 키 설정
OPENAI_API_KEY=your-openai-api-key
GOOGLE_NEWS_API_KEY=your-google-news-api-key
```

### 선택적 환경 변수
```bash
# 서버 설정
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=8501

# OpenAI 설정
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# 크롤링 설정
CRAWLING_INTERVAL=3600  # 초 단위
MAX_RETRIES=3
TIMEOUT=30

# 토큰 사용량 제한
FREE_PLAN_TOKEN_LIMIT=100000  # 월간 토큰 제한
PREMIUM_PLAN_TOKEN_LIMIT=1000000
API_RATE_LIMIT_FREE=10  # 분당 요청 제한
API_RATE_LIMIT_PREMIUM=50

# 로깅 설정
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=app.log

# Nginx 설정
NGINX_HOST=your-domain.com
NGINX_SSL_CERT=/etc/nginx/ssl/cert.pem
NGINX_SSL_KEY=/etc/nginx/ssl/key.pem

# 프론트엔드 설정
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### 환경별 설정

#### 개발 환경
```bash
APP_ENV=development
DEBUG=True
ENABLE_SWAGGER=True
ENABLE_REDOC=True
ENABLE_DEBUG_TOOLBAR=True
```

#### 프로덕션 환경
```bash
APP_ENV=production
DEBUG=False
ENABLE_SWAGGER=False
ENABLE_REDOC=False
ENABLE_DEBUG_TOOLBAR=False
```

#### 테스트 환경
```bash
APP_ENV=testing
DEBUG=True
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost/test_news_analysis
TEST_OPENAI_API_KEY=your-test-openai-api-key
TEST_GOOGLE_NEWS_API_KEY=your-test-google-news-api-key
```

### 보안 주의사항
1. `.env` 파일은 절대 버전 관리에 포함하지 않습니다.
2. 프로덕션 환경의 비밀 키는 안전하게 관리합니다.
3. API 키는 정기적으로 로테이션합니다.
4. 민감한 정보는 환경 변수로 관리합니다.
