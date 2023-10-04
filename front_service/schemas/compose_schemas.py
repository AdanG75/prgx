from typing import List

from pydantic import Field

from schemas.user_schema import UserRequest, UserResponse
from schemas.address_schema import AddressRequest, AddressResponse


class UserRequestAddresses(UserRequest):
    addresses: List[AddressRequest] = Field(..., min_items=1, max_items=19)


class UserResponseAddress(UserResponse):
    addresses: List[AddressResponse] = Field(..., min_items=1, max_items=19)

    model_config = {
        "from_attributes": True
    }


class AddressRequestUsers(AddressRequest):
    users: List[UserRequest] = Field(..., min_items=1, max_items=19)


class AddressResponseUser(AddressResponse):
    users: List[UserResponse] = Field(..., min_items=1, max_items=19)

    model_config = {
        "from_attributes": True
    }
