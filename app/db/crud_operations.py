from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date, timezone
from app.db.models import User, AIUsage
from firebase_admin import auth


# User CRUD operations
def get_or_create_user(db: Session, uid: str, email: str, display_name: str = None, 
                      photo_url: str = None, email_verified: bool = False) -> User:
    """Get existing user or create new one from Firebase data"""
    
    user = db.query(User).filter(User.uid == uid).first()
    
    if user:
        user.last_login = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)
        if display_name and user.display_name != display_name:
            user.display_name = display_name
        if photo_url and user.photo_url != photo_url:
            user.photo_url = photo_url
        if email_verified != user.email_verified:
            user.email_verified = email_verified
        db.commit()
        db.refresh(user)
        return user
    
    # Create new user
    user = User(
        uid=uid,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        email_verified=email_verified,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_uid(db: Session, uid: str) -> User:
    """Get user by Firebase UID"""
    return db.query(User).filter(User.uid == uid).first()

def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def update_user_role(db: Session, uid: str, role: str) -> User:
    """Update user role"""
    user = db.query(User).filter(User.uid == uid).first()
    if user:
        user.role = role
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
    return user

def update_user_plan(db: Session, uid: str, plan: str) -> User:
    """Update user plan"""
    user = db.query(User).filter(User.uid == uid).first()
    if user:
        user.plan = plan
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
    return user

# Usage CRUD operations
def get_usage(db: Session, user_id: str) -> AIUsage:
    """Get usage data for a user for today"""
    return db.query(AIUsage).filter(
        and_(AIUsage.user_id == user_id, AIUsage.date == date.today())
    ).first()

def increment_usage(db: Session, user_id: str, tokens: int = 0) -> AIUsage:
    """Increment usage for a user"""
    # Try to get existing usage record
    usage = get_usage(db, user_id)
    
    if usage:
        # Update existing record
        usage.messages_used += 1
        usage.tokens_used += tokens
        usage.updated_at = datetime.now(timezone.utc)
    else:
        # Create new usage record
        usage = AIUsage(
            user_id=user_id,
            date=date.today(),
            messages_used=1,
            tokens_used=tokens,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(usage)
    
    db.commit()
    db.refresh(usage)
    return usage

def get_user_usage_history(db: Session, user_id: str, days: int = 30):
    """Get usage history for a user"""
    from datetime import timedelta
    
    start_date = date.today() - timedelta(days=days)
    return db.query(AIUsage).filter(
        and_(
            AIUsage.user_id == user_id,
            AIUsage.date >= start_date
        )
    ).order_by(AIUsage.date.desc()).all()
