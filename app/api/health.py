from fastapi import APIRouter, Depends
from app.core.auth import require_user
from app.core.rate_limit import enforce_usage
from app.db.connection import get_db
from app.db.crud_operations import increment_usage

router = APIRouter()


@router.get("/health")
def health(user=Depends(require_user), db=Depends(get_db)):
    enforce_usage(user, db)
    increment_usage(db, user["uid"])
    return {"status": "ok"}
