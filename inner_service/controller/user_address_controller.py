from typing import List

from sqlalchemy.orm import Session

from data.local.orm import orm_user_address
from data.local.orm.orm_address import is_address_dropped
from data.local.orm.orm_user import is_user_dropped
from schemas.user_address_schema import UserAddressResponse
from schemas.user_schema import UserResponse


def assign_relationship_user_address(
        db: Session, id_user: int, id_address: int, execute: str = "now"
) -> UserAddressResponse:
    is_address_erased = is_address_dropped(db, id_address)
    is_user_erased = is_user_dropped(db, id_user)
    valid = not (is_address_erased or is_user_erased)

    db_user_address = orm_user_address.assign_relationship_user_address(db, id_user, id_address, valid, execute)

    return UserAddressResponse.model_validate(db_user_address)


def get_users_by_country(db: Session, country: str) -> List[UserResponse]:
    db_users = orm_user_address.get_users_by_country(db, country)
    users = []

    for db_user in db_users:
        users.append(UserResponse.model_validate(db_user))

    return users
