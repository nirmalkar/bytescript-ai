from fastapi import APIRouter, Depends
from app.core.auth import require_user

router = APIRouter()


@router.get("/health")
def health(user=Depends(require_user)):
    return {
        "status": "ok",
        "user_id": user["uid"],
        "email": user["email"],
    }
