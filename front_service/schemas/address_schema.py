from typing import Optional, List

from pydantic import BaseModel, Field

from front_service.schemas.user_schema import UserRequest, UserResponse


class AddressBase(BaseModel):
    address_1: str = Field(..., min_length=4, max_length=79)
    address_2: Optional[str] = Field(None, min_length=1, max_length=79)
    city: Optional[str] = Field(None, min_length=1, max_length=79)
    state: str = Field(..., min_length=1, max_length=79)
    zip_code: str = Field(..., min_length=4, max_length=8)
    country: str = Field(..., min_length=2, max_length=49)


class AddressRequest(AddressBase):
    pass


class AddressRequestUsers(AddressRequest):
    users: List[UserRequest] = Field(..., min_items=1, max_items=19)


class AddressResponse(AddressBase):
    id_address: int = Field(..., gt=0)
    dropped: bool = Field(False)


class AddressResponseUser(AddressResponse):
    users: List[UserResponse] = Field(..., min_items=1, max_items=19)
