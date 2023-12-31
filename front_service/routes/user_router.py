from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query, status

from controller import user_controller
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
        test: bool = Query(False)
) -> List[UserResponse]:
    """
        GET all users of the system

        **Query Parameter**
        - country(str): Refers the name of a country. When it is passed, the endpoint return all
        users of the selected country

        **Response**
        - Return a response body of type List[\'UserResponse\'] with status code 200
    """
    if country is None:
        response = user_controller.get_users(test)
    else:
        response = user_controller.get_users_by_country(country, test)

    return response


@router.get(
    path="/{id_user}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Get a user via its ID"
)
async def get_user(
        id_user: int = Path(..., gt=0),
        test: bool = Query(False)
) -> UserResponse:
    """
    GET a user with specific ID

    **Response**
    - Return a response body of type \'UserResponse\' with status code 200
    """
    response = user_controller.get_user_by_id(id_user, test)

    return response


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Create a User"
)
async def create_user(
        user_schema: UserRequest = Body(...),
        test: bool = Query(False)
) -> UserResponse:
    """
        POST a user using the request body sent by the customer

        **Body parameter**
        - The structure of the body parameter correspond to \'UserRequest\' schema

        **Response**
        - Return a response body of type \'UserResponse\' with status code 201
    """
    response = user_controller.create_user(user_schema, test)

    return response


@router.post(
    path="/address-batch",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseAddress,
    summary="Create a User with its addresses"
)
async def create_user_with_addresses(
        user_schema: UserRequestAddresses = Body(...),
        test: bool = Query(False)
) -> UserResponseAddress:
    """
        POST a user with its addresses, using the request body sent by the customer

        **Body parameter**
        - The structure of the body parameter correspond to \'UserRequestAddresses\' schema

        **Response**
        - Return a response body of type \'UserResponseAddress\' with status code 201
    """
    response = user_controller.create_user_with_addresses(user_schema, test)

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
        test: bool = Query(False)
) -> UserResponse:
    """
        PATCH a user in order to update its data

        **Path parameter**
        - id_user(int): Field that specify the user to be updated

        **Body parameter**
        - The structure of the body parameter correspond to \'UserRequest\' schema

        **Response**
        - Return a response body of type \'UserResponse\' with status code 200
    """
    response = user_controller.update_user(id_user, user_schema, test)

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
        test: bool = Query(False)
) -> BasicResponse:
    """
        PUT an address into a user

        **Path parameter**
        - id_user(int): Field that specify the target user
        - id_address(int): Field that specify the address which will be assigned into the target user

        **Response**
        - Return a response body of type \'BasicResponse\' with status code 201
    """
    response = user_controller.assign_address_into_user(id_user, id_address, test)

    return response


@router.delete(
    path="/{id_user}",
    status_code=status.HTTP_200_OK,
    response_model=BasicResponse,
    summary="Delete a specific user"
)
async def delete_user(
        id_user: int = Path(..., gt=0),
        test: bool = Query(False)
) -> BasicResponse:
    """
        DELETE the user with specific ID

        **Path parameter**
        - id_user(int): Field that specify the user to be deleted

        **Response**
        - Return a response body of type \'BasicResponse\' with status code 200
    """
    response = user_controller.delete_user(id_user, test)

    return response
