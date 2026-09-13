from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore
from fastapi.security import OAuth2PasswordBearer # type: ignore

from sqlalchemy.orm import Session # type: ignore

from app.dependencies import get_db

from app.auth.jwt_handler import verify_access_token

from app.models.session_model import SessionLog
from app.models.user_model import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == payload.get("user_id")
    ).first()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

def get_current_session(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if payload is None:
    
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    session = db.query(SessionLog).filter(
        SessionLog.session_id == payload.get("session_id")
    ).first()

    if session is None:
    
        raise HTTPException(
            status_code=401,
            detail="Session not found"
        )

    if session.status == "LOGGED_OUT":
        raise HTTPException(
            status_code=403,
            detail="You are Logged out! Please Login to continue."
        )
    
    return session