import asyncio
from http import HTTPStatus
from typing import Annotated, Callable, List
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.dependencies.session_dep import SessionDep
from app.enums.role_enum import UserRole
from app.models.app_user_model import AppUser
from app.utils.auth_utils import verify_extract_user_id


http_bearer_schema = HTTPBearer()


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer_schema)],
    session: SessionDep,
) -> AppUser:
    from app.services.user_service import (
        find_by_id,
    )  # Import here to avoid circular import

    user_id, is_success, err_str = verify_extract_user_id(token.credentials)
    if not is_success:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=err_str,
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await asyncio.to_thread(find_by_id, user_id, session)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Detach user from session
    session.expunge(user)

    return user


def auth_with_any_role(roles: List[UserRole]) -> Callable:
    def checker(user: Annotated[AppUser, Depends(get_current_user)]):
        if roles is not None:
            has_access = False
            user_roles = user.roles.split(",")
            for r in user_roles:
                if r in roles:
                    has_access = True
                    break
            if not has_access:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Does not have enough access",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        return user

    return checker


AuthDepsOnly = Depends(get_current_user) # for router which do not support Annotation
AuthDeps = Annotated[AppUser, Depends(get_current_user)]
AuthAdminOnlyDeps = Annotated[AppUser, Depends(auth_with_any_role([UserRole.ADMIN]))]
AuthUserOnlyDeps = Annotated[AppUser, Depends(auth_with_any_role([UserRole.USER]))]
