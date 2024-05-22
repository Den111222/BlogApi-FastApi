from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.responses import RedirectResponse

from models.schemas.token import Tokens
from models.schemas.user import CreateUser, User, LoginUser
from services.user_service import UserService, get_user_service
from services.token_service import TokenService, get_token_service

router = APIRouter()


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="User registration.",
    description="User registration.",
)
async def signup(
    request: Request,
    _user: CreateUser,
    user_services: UserService = Depends(get_user_service),
):
    """User registration."""

    is_exists = await user_services.check_is_exists(_user.login, _user.email)

    if is_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Login are used"
        )

    user = await user_services.create_user(_user)

    return user


@router.post(
    "/auth",
    response_model=Tokens,
    status_code=status.HTTP_200_OK,
    summary="Login User.",
    description="Login User (get user's tokens: access_token, refresh_token).",
)
async def login_user(
    request: Request,
    response: Response,
    _user: LoginUser,
    user_services: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
) -> Tokens:
    """User login."""

    user = await user_services.check_credentials(_user.login, _user.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login or password"
        )

    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated",
        )

    payload = {
        "service_name": "auth_service",
        **user.model_dump(mode="json", exclude={"login"}),
    }
    tokens = await token_service.create_token(user.login, payload=payload)

    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)

    return tokens


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    request: Request,
    response: Response,
    token_service: TokenService = Depends(get_token_service),
) -> None:
    refresh = request.cookies.get("refresh_token")
    access = request.cookies.get("access_token")

    await token_service.deactivate_tokens(refresh=refresh, access=access)

    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")


@router.post(
    "/refresh",
    response_model=Tokens,
    status_code=status.HTTP_200_OK,
    summary="Refresh User access token.",
    description="Refresh User access token.",
)
async def refresh_token(
    request: Request,
    response: Response,
    user_services: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
) -> Tokens | RedirectResponse:
    """refresh token."""

    refresh = request.cookies.get("refresh_token")

    if refresh is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="There is no refresh token"
        )

    payload = await token_service.check_token(refresh)

    if payload is None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is expired"
        )

    user = await user_services.get_user_by_login(payload.login)

    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated",
        )

    new_payload = {
        "service_name": "auth_service",
        **user.model_dump(mode="json", exclude={"login"}),
    }

    tokens = await token_service.create_token(payload.login, payload=new_payload)

    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)

    return tokens
