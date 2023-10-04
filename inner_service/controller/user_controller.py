from typing import List

from sqlalchemy.orm import Session

from data.local.orm import orm_user
from schemas.user_schema import UserResponse, UserRequest


def get_users(db: Session) -> List[UserResponse]:
    db_users = orm_user.get_all_users(db)
    users = []

    for db_user in db_users:
        users.append(UserResponse.model_validate(db_user))

    return users


def get_user_by_id(db: Session, id_user: int) -> UserResponse:
    db_user = orm_user.get_user_by_id(db, id_user)

    return UserResponse.model_validate(db_user)


def create_user(db: Session, user: UserRequest, execute: str = "now") -> UserResponse:
    db_user = orm_user.create_user(db, user, execute)

    return UserResponse.model_validate(db_user)


def update_user(db: Session, id_user: int, user: UserRequest, execute: str = "now") -> UserResponse:
    db_user = orm_user.update_user(db, id_user, user, execute)

    return UserResponse.model_validate(db_user)


def delete_user(db: Session, id_user: int, execute: str = "now") -> UserResponse:
    db_user = orm_user.delete_user(db, id_user, execute)

    return UserResponse.model_validate(db_user)
