import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import FIREBASE_CREDENTIALS_PATH
from app.db.connection import get_db
from app.db.crud_operations import get_or_create_user

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    """
    - Verifies Firebase ID token
    - Extracts user identity
    - Syncs user to PostgreSQL database
    - Returns user data with role and plan
    """

    token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )

    # Get user record from Firebase
    try:
        firebase_user = auth.get_user(decoded_token["uid"])
        custom_claims = firebase_user.custom_claims or {}
        firebase_role = custom_claims.get("role", "user")
    except Exception:
        # Fallback to token claims if Firebase user record fails
        firebase_role = decoded_token.get("role", "user")
        firebase_user = None

    # Sync user to PostgreSQL
    try:
        db_user = get_or_create_user(
            db=db,
            uid=decoded_token["uid"],
            email=decoded_token.get("email"),
            display_name=decoded_token.get("name") or (firebase_user.display_name if firebase_user else None),
            photo_url=decoded_token.get("picture") or (firebase_user.photo_url if firebase_user else None),
            email_verified=decoded_token.get("email_verified", False) or (firebase_user.email_verified if firebase_user else False)
        )
        
        # Use role from PostgreSQL if set, otherwise from Firebase
        role = db_user.role if db_user.role != "user" else firebase_role
        
        # Update PostgreSQL role if Firebase has different role
        if firebase_role != "user" and db_user.role != firebase_role:
            from app.db.crud_operations import update_user_role
            update_user_role(db, db_user.uid, firebase_role)
            role = firebase_role
            
    except Exception as e:
        # Fallback to Firebase data if database sync fails
        print(f"Warning: Failed to sync user to database: {str(e)}")
        role = firebase_role

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
