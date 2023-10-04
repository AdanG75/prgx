from typing import List

from data.remote import user_data_remote
from schemas.user_schema import UserResponse, UserRequest
from schemas.compose_schemas import UserRequestAddresses, UserResponseAddress
from schemas.generic_schemas import BasicResponse


def get_users(test: bool = False) -> List[UserResponse]:
    data = user_data_remote.get_users(test)

    users = []
    for element in data:
        users.append(UserResponse.model_validate(element))

    return users


def get_users_by_country(country: str, test: bool = False) -> List[UserResponse]:
    data = user_data_remote.get_users_by_country(country, test)

    addresses = []
    for element in data:
        addresses.append(UserResponse.model_validate(element))

    return addresses


def get_user_by_id(id_user: int, test: bool = False) -> UserResponse:
    data = user_data_remote.get_user_by_id(id_user, test)

    return UserResponse.model_validate(data)


def create_user(user: UserRequest, test: bool = False) -> UserResponse:
    data = user_data_remote.create_user(user.model_dump(), test)

    return UserResponse.model_validate(data)


def update_user(id_user: int, user: UserRequest, test: bool = False) -> UserResponse:
    data = user_data_remote.update_user(id_user, user.model_dump(), test)

    return UserResponse.model_validate(data)


def delete_user(id_user: int, test: bool = False) -> BasicResponse:
    data = user_data_remote.delete_user(id_user, test)

    return BasicResponse.model_validate(data)


def assign_address_into_user(id_user: int, id_address: int, test: bool = False) -> BasicResponse:
    data = user_data_remote.assign_address_to_user(id_user, id_address, test)

    return BasicResponse.model_validate(data)


def create_user_with_addresses(user: UserRequestAddresses, test: bool = False) -> UserResponseAddress:
    data = user_data_remote.create_user_with_addresses(user.model_dump(), test)

    return UserResponseAddress.model_validate(data)

