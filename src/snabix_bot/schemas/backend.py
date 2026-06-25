from pydantic import BaseModel, ConfigDict


class BackendHealthDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    ok: bool = True
    status: int = 200
    message: str = "Backend is available."
