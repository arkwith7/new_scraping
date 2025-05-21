#!/bin/bash

# 데이터 디렉토리 생성
sudo mkdir -p /data/postgres
sudo chown -R 999:999 /data/postgres  # PostgreSQL 사용자 권한 설정

# SSL 인증서 디렉토리 생성
sudo mkdir -p nginx/ssl
sudo mkdir -p nginx/logs

# Let's Encrypt 인증서 발급 (도메인이 있는 경우)
if [ ! -z "$DOMAIN" ]; then
    sudo certbot certonly --standalone -d $DOMAIN
    sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/cert.pem
    sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/key.pem
fi

# Docker Compose 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f 