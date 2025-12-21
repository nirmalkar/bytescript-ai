from fastapi import HTTPException, status, Depends
from app.db.connection import get_db
from app.db.crud_operations import get_usage
from app.core.plans import get_daily_limit


def enforce_usage(user, db=Depends(get_db)):
    if user["role"] == "admin":
        return

    usage = get_usage(db, user["uid"])
    used = usage.messages_used if usage else 0

    limit = get_daily_limit(user["plan"])

    if used >= limit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Free tier limit reached. Please upgrade.",
        )
