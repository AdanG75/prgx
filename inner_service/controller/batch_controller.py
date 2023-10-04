from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from controller.user_address_controller import batch_assign_user_address
from data.local.orm import orm_address, orm_user
from controller.exceptions_controller import GENERIC_DB_EXCEPTION
from schemas.address_schema import AddressResponse
from schemas.compose_schemas import UserRequestAddresses, UserResponseAddress, AddressRequestUsers, AddressResponseUser
from schemas.user_schema import UserResponse


def create_user_with_addresses(db: Session, user: UserRequestAddresses) -> UserResponseAddress:
    try:
        db_user = orm_user.create_user(db, user, execute="wait")
        nested = db.begin_nested()
        db.refresh(db_user)

        db_response_addresses = []
        for address in user.addresses:
            db_address = orm_address.create_address(db, address, execute="wait")
            db_response_addresses.append(db_address)

        nested.commit()
        db.commit()

    except Exception as e:
        db.rollback()
        print(e)
        raise GENERIC_DB_EXCEPTION

    else:
        response_addresses = []
        for db_address in db_response_addresses:
            db.refresh(db_address)
            response_addresses.append(AddressResponse.model_validate(db_address))

        batch_assign_user_address(db, "user", db_user.id, response_addresses)

        return UserResponseAddress(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            dropped=db_user.dropped,
            addresses=response_addresses
        )


def create_address_with_users(db: Session, address: AddressRequestUsers) -> AddressResponseUser:
    try:
        db_address = orm_address.create_address(db, address, execute="wait")
        nested = db.begin_nested()
        db.refresh(db_address)

        db_response_users = []
        for user in address.users:
            db_user = orm_user.create_user(db, user, execute="wait")
            db_response_users.append(db_user)

        nested.commit()
        db.commit()

    except Exception as e:
        db.rollback()
        print(e)
        raise GENERIC_DB_EXCEPTION

    else:
        response_users = []
        for db_user in db_response_users:
            db.refresh(db_user)
            response_users.append(UserResponse.model_validate(db_user))

        batch_assign_user_address(db, "address", db_address.id, response_users)

        return AddressResponseUser(
            id=db_address.id,
            address_1=db_address.address_1,
            address_2=db_address.address_2,
            city=db_address.city,
            state=db_address.state,
            zip_code=db_address.zip_code,
            country=db_address.country,
            dropped=db_address.dropped,
            users=response_users
        )
