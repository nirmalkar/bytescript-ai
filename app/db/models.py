from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    uid = Column(String, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String)
    photo_url = Column(String)
    email_verified = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    role = Column(String, default="user")  # admin, user
    plan = Column(String, default="FREE")  # FREE, PAID
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime)


class AIUsage(Base):
    __tablename__ = "ai_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)
    date = Column(Date, nullable=False)
    messages_used = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
        Index('idx_user_date', 'user_id', 'date'),
    )
