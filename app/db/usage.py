from app.db.connection import get_db
from app.db.crud_operations import get_usage, increment_usage
from fastapi import Depends

# Re-export functions for backward compatibility
def get_usage_with_db(user_id: str, db=Depends(get_db)):
    """Get usage data for a user for today"""
    return get_usage(db, user_id)

def increment_usage_with_db(user_id: str, tokens: int = 0, db=Depends(get_db)):
    """Increment usage for a user"""
    return increment_usage(db, user_id, tokens)

# Legacy exports for compatibility
__all__ = ['get_usage', 'increment_usage']
