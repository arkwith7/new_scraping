from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    plan_type: Optional[str] = "free"

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    total_tokens_used: int = 0
    monthly_tokens_used: int = 0
    last_token_reset: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TokenUsageBase(BaseModel):
    tokens_used: int
    operation_type: str

class TokenUsageCreate(TokenUsageBase):
    pass

class TokenUsage(TokenUsageBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True 