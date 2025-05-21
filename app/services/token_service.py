from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import User, TokenUsage
from app.schemas.user import TokenUsageCreate

class TokenService:
    def __init__(self, db: Session):
        self.db = db

    def update_token_usage(
        self,
        user_id: int,
        tokens_used: int,
        operation_type: str
    ) -> TokenUsage:
        """토큰 사용량을 업데이트하고 기록합니다."""
        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # 토큰 사용량 기록 생성
        token_usage = TokenUsage(
            user_id=user_id,
            tokens_used=tokens_used,
            operation_type=operation_type
        )
        self.db.add(token_usage)

        # 사용자 총 토큰 사용량 업데이트
        user.total_tokens_used += tokens_used
        user.monthly_tokens_used += tokens_used

        # 월간 토큰 사용량 리셋 확인
        if user.last_token_reset and (datetime.now() - user.last_token_reset) > timedelta(days=30):
            user.monthly_tokens_used = tokens_used
            user.last_token_reset = datetime.now()
        elif not user.last_token_reset:
            user.last_token_reset = datetime.now()

        self.db.commit()
        self.db.refresh(token_usage)
        return token_usage

    def get_user_token_usage(
        self,
        user_id: int,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> list[TokenUsage]:
        """사용자의 토큰 사용량 기록을 조회합니다."""
        query = self.db.query(TokenUsage).filter(TokenUsage.user_id == user_id)
        
        if start_date:
            query = query.filter(TokenUsage.created_at >= start_date)
        if end_date:
            query = query.filter(TokenUsage.created_at <= end_date)
            
        return query.order_by(TokenUsage.created_at.desc()).all()

    def get_user_token_stats(self, user_id: int) -> dict:
        """사용자의 토큰 사용량 통계를 조회합니다."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # 최근 30일간의 토큰 사용량 조회
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_usage = self.db.query(TokenUsage)\
            .filter(
                TokenUsage.user_id == user_id,
                TokenUsage.created_at >= thirty_days_ago
            ).all()

        # 작업 유형별 토큰 사용량 집계
        usage_by_type = {}
        for usage in recent_usage:
            if usage.operation_type not in usage_by_type:
                usage_by_type[usage.operation_type] = 0
            usage_by_type[usage.operation_type] += usage.tokens_used

        return {
            "total_tokens_used": user.total_tokens_used,
            "monthly_tokens_used": user.monthly_tokens_used,
            "last_token_reset": user.last_token_reset,
            "usage_by_type": usage_by_type
        }

    def check_token_limit(self, user_id: int, required_tokens: int) -> bool:
        """사용자의 토큰 사용량 제한을 확인합니다."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # 요금제별 월간 토큰 제한
        monthly_limits = {
            "free": 100000,  # 10만 토큰
            "premium": 1000000  # 100만 토큰
        }

        limit = monthly_limits.get(user.plan_type, 100000)
        return user.monthly_tokens_used + required_tokens <= limit 