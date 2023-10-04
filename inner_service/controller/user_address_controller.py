from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from controller.exceptions_controller import GENERIC_DB_EXCEPTION
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


def batch_assign_user_address(db: Session, single_type: str, id_item: int, base_items: List[BaseModel]):
    try:
        nested = db.begin_nested()
        if single_type == "user":
            for address in base_items:
                assign_relationship_user_address(db, id_item, address.id, execute="wait")
        elif single_type == "address":
            for user in base_items:
                assign_relationship_user_address(db, user.id, id_item, execute="wait")
        else:
            return

        nested.commit()
        db.commit()

    except Exception as e:
        db.rollback()
        print(e)
        raise GENERIC_DB_EXCEPTION


def get_users_by_country(db: Session, country: str) -> List[UserResponse]:
    db_users = orm_user_address.get_users_by_country(db, country)
    users = []

    for db_user in db_users:
        users.append(UserResponse.model_validate(db_user))

    return users
