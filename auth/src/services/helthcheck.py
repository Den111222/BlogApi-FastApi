from sqlalchemy.ext.asyncio import AsyncSession

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
