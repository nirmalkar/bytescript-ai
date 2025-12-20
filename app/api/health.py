from fastapi import APIRouter, Depends
from app.core.auth import require_user
from app.core.rate_limit import enforce_usage
from app.db.usage import increment_usage

router = APIRouter()


@router.get("/health")
def health(user=Depends(require_user)):
    enforce_usage(user)
    increment_usage(user["uid"])
    return {"status": "ok"}
