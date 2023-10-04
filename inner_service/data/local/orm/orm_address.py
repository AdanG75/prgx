from typing import List, Type

from sqlalchemy.orm import Session

from controller.exceptions_controller import NOT_FOUND
from data.local.orm.orm_common import _commit_changes
from data.local.models.db_address import DBAddress
from schemas.address_schema import AddressRequest


def get_all_addresses(db: Session) -> List[Type[DBAddress]]:
    addresses: List[Type[DBAddress]] = db.query(DBAddress).where(DBAddress.dropped == False).all()

    return addresses


def get_address_by_id(db: Session, id_address: int, dropped: bool = False) -> Type[DBAddress]:
    if dropped:
        address: Type[DBAddress] = db.query(DBAddress).where(DBAddress.id == id_address).one_or_none()
    else:
        address: Type[DBAddress] = (db.query(DBAddress)
                                    .where(
                                        DBAddress.id == id_address,
                                        DBAddress.dropped == False
                                    ).one_or_none())

    if address is None:
        raise NOT_FOUND

    return address


def get_address_by_country(db: Session, country: str) -> List[Type[DBAddress]]:
    addresses: List[Type[DBAddress]] = (db.query(DBAddress)
                                        .where(
                                            DBAddress.country == country,
                                            DBAddress.dropped == False
                                        ).all())

    return addresses


def is_address_dropped(db: Session, id_address: int) -> bool:
    db_address = get_address_by_id(db, id_address, True)

    return db_address.dropped


def create_address(db: Session, address: AddressRequest, execute: str = "now") -> DBAddress:
    new_address = DBAddress(
        address_1=address.address_1,
        address_2=address.address_2,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
        country=address.country,
        dropped=False
    )

    new_address = _commit_changes(db, new_address, execute)

    return new_address


def update_address(db: Session, id_address: int, address: AddressRequest, execute: str = "now") -> DBAddress:
    db_address = get_address_by_id(db, id_address)

    db_address.address_1 = address.address_1 if address.address_1 is not None else db_address.address_1
    db_address.address_2 = address.address_2 if address.address_2 is not None else db_address.address_2
    db_address.city = address.city if address.city is not None else db_address.city
    db_address.state = address.state if address.state is not None else db_address.state
    db_address.zip_code = address.zip_code if address.zip_code is not None else db_address.zip_code
    db_address.country = address.country if address.country is not None else db_address.country

    db_address = _commit_changes(db, db_address, execute)

    return db_address


def delete_address(db: Session, id_address: int, execute: str = "now") -> DBAddress:
    db_address = get_address_by_id(db, id_address)

    db_address.dropped = True

    db_address = _commit_changes(db, db_address, execute)

    return db_address
