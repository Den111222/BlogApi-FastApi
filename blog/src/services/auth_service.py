import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import app_settings


def decode_token(jwt_token: str) -> dict | None:
    # Решил применить симитричное шифрование, не критично
    # Decided to apply simitric encryption, not critical
    key = app_settings.token_secret
    try:
        decoded = jwt.decode(jwt_token, key, algorithms=app_settings.algorithm)
        return decoded
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization request",
            )
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only Bearer token might be accepted",
            )
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        return decoded_token

    def parse_token(self, jwt_token: str) -> dict | None:
        return decode_token(jwt_token)


security_jwt = JWTBearer()
