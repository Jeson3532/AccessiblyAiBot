from pydantic import BaseModel, Field
from starlette.responses import FileResponse
from typing import Union


class FailedResponse(BaseModel):
    status_code: int = Field(...)
    detail: Union[str, dict] = Field(...)
class SuccessResponse(BaseModel):
    status_code: int = Field(200)
    data: Union[str, dict] = Field(None)