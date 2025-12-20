import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import FIREBASE_CREDENTIALS_PATH

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    - Verifies Firebase ID token
    - Extracts user identity
    - Adds role and plan from Firebase custom claims
    """

    token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )

    # Get user record to access custom claims
    try:
        user_record = auth.get_user(decoded_token["uid"])
        custom_claims = user_record.custom_claims or {}
        role = custom_claims.get("role", "user")
    except Exception:
        role = decoded_token.get("role", "user")

    return {
        "uid": decoded_token["uid"],
        "email": decoded_token.get("email"),
        "role": role,
        "plan": "FREE",  # temporary, later loaded from DB
    }


def require_user(user=Depends(get_current_user)):
    """
    Semantic alias.
    Explicitly says: this endpoint requires authentication.
    """
    return user
