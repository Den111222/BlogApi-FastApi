from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import get_session
from models.schemas.healthcheck import HealthCheck


class HealthCheckService:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    async def get_status() -> HealthCheck:
        response = {
            "status": "OK",
            "message": "Service is available right now.",
        }
        return HealthCheck(**response)


def get_file_service(
    _session: AsyncSession = Depends(get_session),
) -> HealthCheckService:
    return HealthCheckService(_session)
