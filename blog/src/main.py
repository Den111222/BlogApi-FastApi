import logging
import uvicorn

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import posts, healthcheck, categories, tags
import constants as const
from core.config import app_settings, LOGGING

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(posts.router)
v1_router.include_router(categories.router)
v1_router.include_router(tags.router)
v1_router.include_router(healthcheck.router)


app = FastAPI(
    title=const.APP_API_DOCS_TITLE,
    version=const.APP_VERSION,
    description=const.APP_DESCRIPTION,
    docs_url="/blog/api/openapi",
    openapi_url="/blog/api/openapi.json",
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
