from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ...core.config import settings
from ...core.security import create_access_token
from ...db.session import get_db
from ...schemas.user import User, UserCreate, UserUpdate, Token, TokenUsage
from ...services import user_service
from ...services.token_service import TokenService
from ...db.models import User as UserModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    return user_service.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    user_service.update_last_login(db, user.id)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db)
):
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    user: UserUpdate,
    current_user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db)
):
    return user_service.update_user(db=db, user_id=current_user.id, user=user)

@router.get("/users", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(user_service.get_current_active_superuser),
    db: Session = Depends(get_db)
):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me/token-usage", response_model=List[TokenUsage])
def get_user_token_usage(
    current_user: UserModel = Depends(user_service.get_current_user),
    db: Session = Depends(get_db)
):
    token_service = TokenService(db)
    return token_service.get_user_token_usage(current_user.id)

@router.get("/me/token-stats")
def get_user_token_stats(
    current_user: UserModel = Depends(user_service.get_current_user),
    db: Session = Depends(get_db)
):
    token_service = TokenService(db)
    return token_service.get_user_token_stats(current_user.id) 