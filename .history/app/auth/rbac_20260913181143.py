from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore

from app.auth.oauth2 import get_current_session, get_current_user


def role_required(allowed_roles: list):

    def checker(
        current_session = Depends(get_current_session),
        current_user = Depends(get_current_user)
    ):
        print(current_session)
        if current_session.status == "LOGGED_OUT":
            raise HTTPException(
                status_code=403,
                detail="You are Logged out! Please Login to continue."
            )

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return current_user

    return checker