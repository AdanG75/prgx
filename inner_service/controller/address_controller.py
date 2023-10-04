from typing import List

from sqlalchemy.orm import Session

from data.local.orm import orm_address
from schemas.address_schema import AddressResponse, AddressRequest


def get_addresses(db: Session) -> List[AddressResponse]:
    db_addresses = orm_address.get_all_addresses(db)
    addresses = []

    for db_address in db_addresses:
        addresses.append(AddressResponse.model_validate(db_address))

    return addresses


def get_address_by_id(db: Session, id_address: int) -> AddressResponse:
    db_address = orm_address.get_address_by_id(db, id_address)

    return AddressResponse.model_validate(db_address)


def get_address_by_country(db: Session, country: str) -> List[AddressResponse]:
    db_addresses = orm_address.get_address_by_country(db, country)
    addresses = []

    for db_address in db_addresses:
        addresses.append(AddressResponse.model_validate(db_address))

    return addresses


def create_address(db: Session, address: AddressRequest, execute: str = "now") -> AddressResponse:
    db_address = orm_address.create_address(db, address, execute)

    return AddressResponse.model_validate(db_address)


def update_address(db: Session, id_address: int, address: AddressRequest, execute:str = "now") -> AddressResponse:
    db_address = orm_address.update_address(db, id_address, address, execute)

    return AddressResponse.model_validate(db_address)


def delete_address(db: Session, id_address: int, execute: str = "now") -> AddressResponse:
    db_address = orm_address.delete_address(db, id_address, execute)

    return AddressResponse.model_validate(db_address)
