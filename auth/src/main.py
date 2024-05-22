import logging
import uvicorn

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from models.schemas.models_base import BaseExceptionBody

from api.v1 import users, healthcheck
import constants as const
from core.config import app_settings, LOGGING

v1_router = APIRouter(
    prefix="/auth/api/v1/users",
    tags=["Users"],
    responses={
        404: {"model": BaseExceptionBody},
        400: {"model": BaseExceptionBody},
    },
)
v1_router.include_router(healthcheck.router)
v1_router.include_router(users.router)

app = FastAPI(
    title=const.APP_API_DOCS_TITLE,
    version=const.APP_VERSION,
    description=const.APP_DESCRIPTION,
    docs_url="/auth/api/openapi",
    openapi_url="/auth/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.host,
        port=app_settings.port,
        log_config=LOGGING,
        log_level=logging.INFO,
    )
