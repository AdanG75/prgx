from typing import List

from data.remote import address_data_remote
from schemas.address_schema import AddressResponse, AddressRequest
from schemas.compose_schemas import AddressRequestUsers, AddressResponseUser
from schemas.generic_schemas import BasicResponse


def get_addresses(test: bool = False) -> List[AddressResponse]:
    data = address_data_remote.get_addresses(test)

    addresses = []
    for element in data:
        addresses.append(AddressResponse.model_validate(element))

    return addresses


def get_address_by_country(country: str, test: bool = False) -> List[AddressResponse]:
    data = address_data_remote.get_addresses_by_country(country, test)

    addresses = []
    for element in data:
        addresses.append(AddressResponse.model_validate(element))

    return addresses


def get_address_by_id(id_address: int, test: bool = False) -> AddressResponse:
    data = address_data_remote.get_address_by_id(id_address, test)

    return AddressResponse.model_validate(data)


def create_address(address: AddressRequest, test: bool = False) -> AddressResponse:
    data = address_data_remote.create_address(address.model_dump(), test)

    return AddressResponse.model_validate(data)


def update_address(id_address: int, address: AddressRequest, test: bool = False) -> AddressResponse:
    data = address_data_remote.update_address(id_address, address.model_dump(), test)

    return AddressResponse.model_validate(data)


def delete_address(id_address: int, test: bool = False) -> BasicResponse:
    data = address_data_remote.delete_address(id_address, test)

    return BasicResponse.model_validate(data)


def assign_user_into_address(id_address: int, id_user: int, test: bool = False) -> BasicResponse:
    data = address_data_remote.assign_user_to_address(id_address, id_user, test)

    return BasicResponse.model_validate(data)


def create_address_with_users(address: AddressRequestUsers, test: bool = False) -> AddressResponseUser:
    data = address_data_remote.create_address_with_users(address.model_dump(), test)

    return AddressResponseUser.model_validate(data)
