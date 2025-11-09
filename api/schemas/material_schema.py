from pydantic import BaseModel, Field


class AddMaterial(BaseModel):
    telegram_id: int = Field(...)
    material_name: str = Field(...)
    material: str = Field(...)
