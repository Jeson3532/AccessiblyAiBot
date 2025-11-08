from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from api.roles.role import UserRoles
from typing import Optional

class AddUserModel(BaseModel):
    telegram_id: int
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[PhoneNumber] = Field(default=None)
    role: UserRoles = Field(default=UserRoles.USER)

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)