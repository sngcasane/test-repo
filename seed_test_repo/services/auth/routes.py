"""Auth endpoints — login, refresh, logout, me."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from .tokens import issue_access_token, rotate_refresh_token, revoke_session
from .users import authenticate, get_user_by_id
from .deps import current_user

router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


@router.post("/login", response_model=TokenPair)
async def login(req: LoginRequest) -> TokenPair:
    user = await authenticate(req.email, req.password)
    if user is None:
        # NB: do not leak which of email/password was wrong — generic 401
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    access = issue_access_token(user.id, user.role)
    refresh = await rotate_refresh_token(user.id, previous=None)
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenPair)
async def refresh(refresh_token: str) -> TokenPair:
    new_refresh = await rotate_refresh_token(user_id=None, previous=refresh_token)
    # rotate_refresh_token raises if the token is invalid or reused
    user = await get_user_by_id(new_refresh.user_id)
    access = issue_access_token(user.id, user.role)
    return TokenPair(access_token=access, refresh_token=new_refresh.token)


@router.post("/logout", status_code=204)
async def logout(user=Depends(current_user)) -> None:
    await revoke_session(user.session_id)


@router.get("/me")
async def me(user=Depends(current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}
