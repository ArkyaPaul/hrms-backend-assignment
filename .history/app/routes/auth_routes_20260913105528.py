from fastapi import APIRouter # type: ignore
from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore
from app.auth.oauth2 import get_current_user # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.dependencies import get_db

from app.models.user_model import User

from app.schemas.user_schema import UserRegister, UserLogin

from app.utils.hash import hash_password, verify_password

from app.auth.jwt_handler import create_access_token, create_refresh_token, verify_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.username
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    valid_password = verify_password(
        user.password,
        existing_user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        {
            "user_id": existing_user.id,
            "role": existing_user.role,
            "email": existing_user.email
        }
    )

    refresh_token = create_refresh_token(
        {
            "user_id": existing_user.id
        }
    )

    new_Se

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_logged_in_user(
    current_user = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@router.post("/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):

    payload = verify_access_token(
        refresh_token
    )

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":

        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )
    
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    new_access_token = create_access_token(
        {
            "user_id": user.id,
            "role": user.role,
            "email": user.email
        }
    )

    return {
        "access_token": new_access_token
    }