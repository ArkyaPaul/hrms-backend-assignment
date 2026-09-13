from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore

from app.auth.oauth2 import get_current_session, get_current_user


def role_required(allowed_roles: list):

    def checker(
        current_session = Depends(get_current_session),
        current_user = Depends(get_current_user)
    ):
        if current_session.status is "L"

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return current_user

    return checker