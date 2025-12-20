from fastapi import HTTPException, status
from app.db.usage import get_usage
from app.core.plans import get_daily_limit


def enforce_usage(user):
    if user["role"] == "admin":
        return

    usage = get_usage(user["uid"])
    used = usage["messages_used"] if usage else 0

    limit = get_daily_limit(user["plan"])

    if used >= limit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Free tier limit reached. Please upgrade.",
        )
