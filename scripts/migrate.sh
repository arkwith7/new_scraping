#!/bin/bash

# 데이터베이스 마이그레이션 스크립트

# 환경 변수 설정
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 마이그레이션 명령어
case "$1" in
    "init")
        echo "초기 마이그레이션 환경 설정..."
        alembic init alembic
        ;;
    "create")
        echo "새로운 마이그레이션 생성..."
        alembic revision --autogenerate -m "$2"
        ;;
    "upgrade")
        echo "데이터베이스 업그레이드..."
        alembic upgrade head
        ;;
    "downgrade")
        echo "데이터베이스 다운그레이드..."
        alembic downgrade -1
        ;;
    "history")
        echo "마이그레이션 히스토리..."
        alembic history
        ;;
    *)
        echo "사용법: $0 {init|create|upgrade|downgrade|history}"
        echo "  init: 초기 마이그레이션 환경 설정"
        echo "  create <message>: 새로운 마이그레이션 생성"
        echo "  upgrade: 데이터베이스 업그레이드"
        echo "  downgrade: 데이터베이스 다운그레이드"
        echo "  history: 마이그레이션 히스토리 조회"
        exit 1
        ;;
esac 