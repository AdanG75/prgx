from typing import List, Type

from sqlalchemy.orm import Session

from data.local.models.db_user_address import DBUserAddress
from data.local.models.db_address import DBAddress
from data.local.models.db_user import DBUser
from data.local.orm.orm_common import _commit_changes


def assign_relationship_user_address(
        db: Session, id_user: int, id_address: int, valid: bool = False, execute: str = "now"
) -> DBUserAddress:
    new_user_address = DBUserAddress(
        id_user=id_user,
        id_address=id_address,
        valid=valid
    )

    new_user_address = _commit_changes(db, new_user_address, execute)

    return new_user_address


def get_users_by_country(db: Session, country: str) -> List[Type[DBUser]]:
    users = (db.query(DBUser).join(DBUserAddress, DBUser.id == DBUserAddress.id_user)
             .join(DBAddress, DBUserAddress.id_address == DBAddress.id)
             .filter(DBUser.dropped == False)
             .filter(DBUserAddress.valid == True)
             .filter(DBAddress.dropped == False)
             .filter(DBAddress.country == country))

    return users
