from fastapi import APIRouter

from models.schemas.healthcheck import HealthCheck
from services.helthcheck import HealthCheckService as service

router = APIRouter(prefix="/healthcheck")


@router.get("/", response_model=HealthCheck, summary="Check status of app")
async def get_service_status() -> HealthCheck:
    """
    Get status of app.
    """
    return await service.get_status()
