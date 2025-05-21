from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, ARRAY, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    plan_type = Column(String, default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # LLM 토큰 사용량 관련 필드
    total_tokens_used = Column(Integer, default=0)
    monthly_tokens_used = Column(Integer, default=0)
    last_token_reset = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    news_data = relationship("NewsData", back_populates="user")
    analysis_results = relationship("AnalysisResult", back_populates="user")
    api_usage = relationship("APIUsage", back_populates="user")
    analysis_history = relationship("AnalysisHistory", back_populates="user")
    comparison_history = relationship("ComparisonHistory", back_populates="user")
    summary_history = relationship("SummaryHistory", back_populates="user")
    token_usage = relationship("TokenUsage", back_populates="user")

class NewsData(Base):
    __tablename__ = "news_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(String)  # google, naver, sk_hynix, samsung_semiconductor
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    published_date = Column(DateTime(timezone=True))
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)
    
    # 관계 설정
    user = relationship("User", back_populates="news_data")
    analysis_results = relationship("AnalysisResult", back_populates="news_data")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    news_ids = Column(JSON)
    keywords = Column(JSON)
    sentiment = Column(JSON)
    topics = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    user = relationship("User", back_populates="analysis_results")
    news_data = relationship("NewsData", back_populates="analysis_results")

class APIUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String)
    request_count = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    user = relationship("User", back_populates="api_usage")

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_type = Column(String)
    text = Column(Text)
    result = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="analysis_history")

class ComparisonHistory(Base):
    __tablename__ = "comparison_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text1 = Column(Text)
    text2 = Column(Text)
    result = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="comparison_history")

class SummaryHistory(Base):
    __tablename__ = "summary_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text)
    max_length = Column(Integer, nullable=True)
    result = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="summary_history")

class TokenUsage(Base):
    __tablename__ = "token_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tokens_used = Column(Integer)
    operation_type = Column(String)  # analyze, compare, summarize
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    user = relationship("User", back_populates="token_usage")

# 관계 설정
User.news_data = relationship("NewsData", back_populates="user")
User.analysis_results = relationship("AnalysisResult", back_populates="user")
User.api_usage = relationship("APIUsage", back_populates="user")
User.analysis_history = relationship("AnalysisHistory", back_populates="user")
User.comparison_history = relationship("ComparisonHistory", back_populates="user")
User.summary_history = relationship("SummaryHistory", back_populates="user")
User.token_usage = relationship("TokenUsage", back_populates="user") 