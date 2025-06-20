from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependency import get_current_user
from app.schemas import CreateUserIn, UserSchema
from app.services import UserService
from app.tools import generate_user_jwt_token

router = APIRouter(prefix="", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(service: Annotated[UserService, Depends()], user: CreateUserIn):
    return await service.create_user(user)


@router.get("/verify/email")
async def verify_email(service: Annotated[UserService, Depends()], token: str) -> UserSchema:
    return await service.verify_email(token)


@router.post("/token")
async def login(
    service: Annotated[UserService, Depends()],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user_jwt_schema = await service.authenticate_user_via_jwt(
        form_data.username, form_data.password
    )
    token = generate_user_jwt_token(user_jwt_schema)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def profile_detail_view(
    current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserSchema:
    return current_user
