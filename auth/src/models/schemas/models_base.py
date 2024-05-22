from pydantic import BaseModel


class BaseResponseBody(BaseModel):
    data: dict | list


class BaseExceptionBody(BaseModel):
    error: dict | str | None = None
