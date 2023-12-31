from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query, status, Depends
from sqlalchemy.orm import Session

from data.database import get_db
from controller import user_controller, user_address_controller, batch_controller
from schemas.user_schema import UserResponse, UserRequest
from schemas.compose_schemas import UserResponseAddress, UserRequestAddresses
from schemas.generic_schemas import BasicResponse

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
    summary="Get all users"
)
async def get_all_users(
        country: Optional[str] = Query(None, min_length=2, max_length=49),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
        GET all users of the system

        **Query Parameter**
        - country(str): Refers the name of a country. When it is passed, the endpoint return all
        users of the selected country
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Response**
        - Return a response body of type List[\'UserResponse\'] with status code 200
    """
    if country is None:
        response = user_controller.get_users(db)
    else:
        response = user_address_controller.get_users_by_country(db, country)

    return response


@router.get(
    path="/{id_user}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Get a user via its ID"
)
async def get_user(
        id_user: int = Path(..., gt=0),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> UserResponse:
    """
    GET a user with specific ID

    **Path Parameter**
    -id_user(int): Field that specify the user to be retrieved

    **Query Parameter**
    - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

    **Response**
    - Return a response body of type \'UserResponse\' with status code 200
    """
    response = user_controller.get_user_by_id(db, id_user)

    return response


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Create a User"
)
async def create_user(
        user_schema: UserRequest = Body(...),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> UserResponse:
    """
        POST a user using the request body sent by the customer

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Body parameter**
        - The structure of the body parameter correspond to \'UserRequest\' schema

        **Response**
        - Return a response body of type \'UserResponse\' with status code 201
    """
    response = user_controller.create_user(db, user_schema)

    return response


@router.post(
    path="/address-batch",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseAddress,
    summary="Create a User with its addresses"
)
async def create_user_with_addresses(
        user_schema: UserRequestAddresses = Body(...),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> UserResponseAddress:
    """
        POST a user with its addresses, using the request body sent by the customer

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Body parameter**
        - The structure of the body parameter correspond to \'UserRequestAddresses\' schema

        **Response**
        - Return a response body of type \'UserResponseAddress\' with status code 201
    """
    response = batch_controller.create_user_with_addresses(db, user_schema)

    return response


@router.patch(
    path="/{id_user}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Update user\'s data"
)
async def update_user(
        id_user: int = Path(..., gt=0),
        user_schema: UserRequest = Body(...),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> UserResponse:
    """
        PATCH a user in order to update its data

        **Path parameter**
        - id_user(int): Field that specify the user to be updated

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Body parameter**
        - The structure of the body parameter correspond to \'UserRequest\' schema

        **Response**
        - Return a response body of type \'UserResponse\' with status code 200
    """
    response = user_controller.update_user(db, id_user, user_schema)

    return response


@router.put(
    path="/{id_user}/address/{id_address}",
    status_code=status.HTTP_201_CREATED,
    response_model=BasicResponse,
    summary="Assign an address to a user"
)
async def assign_address_to_user(
        id_user: int = Path(..., gt=0),
        id_address: int = Path(..., gt=0),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> BasicResponse:
    """
        PUT an address into a user

        **Path parameter**
        - id_user(int): Field that specify the target user
        - id_address(int): Field that specify the address which will be assigned into the target user

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Response**
        - Return a response body of type \'BasicResponse\' with status code 201. If successful is False means that
        assign was created but an element or both, user or address, are dropped.
    """
    result = user_address_controller.assign_relationship_user_address(db, id_user, id_address)

    return BasicResponse(
        operation="Assign address to user",
        successful=result.valid
    )


@router.delete(
    path="/{id_user}",
    status_code=status.HTTP_200_OK,
    response_model=BasicResponse,
    summary="Delete a specific user"
)
async def delete_user(
        id_user: int = Path(..., gt=0),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> BasicResponse:
    """
        DELETE the user with specific ID

        **Path parameter**
        - id_user(int): Field that specify the user to be deleted

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Response**
        - Return a response body of type \'BasicResponse\' with status code 200
    """
    result = user_controller.delete_user(db, id_user)

    return BasicResponse(
        operation="Delete user",
        successful=result.dropped
    )
