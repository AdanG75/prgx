from typing import List

from pydantic import BaseModel, Field, EmailStr

from front_service.schemas.address_schema import AddressRequest, AddressResponse


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=79)
    last_name: str = Field(..., min_length=1, max_length=79)
    email: EmailStr = Field(...)


class UserRequest(UserBase):
    password: str = Field(..., min_length=8, max_length=63)


class UserRequestAddresses(UserRequest):
    addresses: List[AddressRequest] = Field(..., min_items=1, max_items=19)


class UserResponse(UserBase):
    id_address: int = Field(..., gt=0)
    dropped: bool = Field(False)


class UserResponseAddress(UserResponse):
    addresses: List[AddressResponse] = Field(..., min_items=1, max_items=19)