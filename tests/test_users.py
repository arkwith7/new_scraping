import pytest
from fastapi import status

def test_create_user(client):
    response = client.post(
        "/users/register",
        json={
            "email": "newuser@example.com",
            "password": "newpassword",
            "full_name": "New User"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data

def test_create_user_existing_email(client, test_user):
    response = client.post(
        "/users/register",
        json={
            "email": test_user.email,
            "password": "newpassword",
            "full_name": "New User"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_user(client, test_user):
    response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_wrong_password(client, test_user):
    response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user(client, test_user):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 현재 사용자 정보 조회
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name

def test_update_user(client, test_user):
    # 로그인하여 토큰 획득
    login_response = client.post(
        "/users/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # 사용자 정보 업데이트
    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": test_user.email,
            "full_name": "Updated Name",
            "password": "newpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name" 