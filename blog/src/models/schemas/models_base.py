from pydantic import BaseModel


class BaseResponseBody(BaseModel):
    data: dict | list
