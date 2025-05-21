import pytest
from fastapi import status
from datetime import datetime, timedelta

@pytest.fixture
def test_news(client, test_user):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 테스트 뉴스 데이터 생성
    news_data = {
        "source": "test_source",
        "title": "Test News Title",
        "content": "This is a test news content.",
        "url": "http://example.com/test",
        "published_date": datetime.now().isoformat(),
        "metadata": {"category": "test"}
    }
    
    response = client.post(
        "/news/",
        headers={"Authorization": f"Bearer {token}"},
        json=news_data
    )
    return response.json()

def test_search_news(client, test_user, test_news):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 뉴스 검색
    response = client.get(
        "/news/search",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "keyword": "test",
            "num_results": 10,
            "date_range": 7,
            "sources": ["test_source"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_count" in data
    assert "results" in data
    assert len(data["results"]) > 0

def test_get_news(client, test_user, test_news):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 특정 뉴스 조회
    response = client.get(
        f"/news/{test_news['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_news["id"]
    assert data["title"] == test_news["title"]

def test_get_user_news(client, test_user, test_news):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 사용자의 뉴스 목록 조회
    response = client.get(
        "/news/user",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(news["id"] == test_news["id"] for news in data)

def test_analyze_news(client, test_user, test_news):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 뉴스 분석
    response = client.post(
        f"/news/{test_news['id']}/analyze",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "keywords" in data
    assert "sentiment" in data
    assert "topics" in data 