from typing import List, Type

from sqlalchemy.orm import Session

from controller.exceptions_controller import NOT_FOUND
from data.local.orm.orm_common import _commit_changes
from data.local.models.db_user import DBUser
from schemas.user_schema import UserRequest


def get_all_users(db: Session) -> List[Type[DBUser]]:
    users: List[Type[DBUser]] = db.query(DBUser).where(DBUser.dropped == False).all()

    return users


def get_user_by_id(db: Session, id_user: int, dropped: bool = False) -> Type[DBUser]:
    if dropped:
        user : Type[DBUser] = db.query(DBUser).where(DBUser.id == id_user).one_or_none()
    else:
        user: Type[DBUser] = (db.query(DBUser)
                               .where(
                                    DBUser.id == id_user,
                                    DBUser.dropped == False
                                ).one_or_none())

    if user is None:
        raise NOT_FOUND

    return user


def is_user_dropped(db: Session, id_user: int) -> bool:
    db_user = get_user_by_id(db, id_user, True)

    return db_user.dropped


def create_user(db: Session, user: UserRequest, execute: str = "now") -> DBUser:
    new_user = DBUser(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        dropped=False
    )

    new_user = _commit_changes(db, new_user, execute)

    return new_user


def update_user(db: Session, id_user: int, user: UserRequest, execute: str = "now") -> DBUser:
    db_user = get_user_by_id(db, id_user)

    db_user.first_name = user.first_name if user.first_name is not None else db_user.first_name
    db_user.last_name = user.last_name if user.last_name is not None else db_user.last_name
    db_user.email = user.email if user.email is not None else db_user.email
    db_user.password = user.password if user.password is not None else db_user.password

    db_user = _commit_changes(db, db_user, execute)

    return db_user


def delete_user(db: Session, id_user: int, execute: str = "now") -> DBUser:
    db_user = get_user_by_id(db, id_user)

    db_user.dropped = True

    db_user = _commit_changes(db, db_user, execute)

    return db_user
