from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query, status, Depends
from sqlalchemy.orm import Session

from controller import address_controller
from data.database import get_db
from schemas.address_schema import AddressResponse, AddressRequest
from schemas.compose_schemas import AddressResponseUser, AddressRequestUsers
from schemas.generic_schemas import BasicResponse

router = APIRouter(prefix="/address", tags=["Address"])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[AddressResponse],
    summary="Get all addresses"
)
async def get_all_addresses(
        country: Optional[str] = Query(None, min_length=2, max_length=49),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> List[AddressResponse]:
    """
        GET all addresses of the system

        **Query Parameter**
        - country(str): Refers the name of a country. When it is passed, the endpoint return all
        addresses of the selected country
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Response**
        - Return a response body of type List[\'AddressResponse\'] with status code 200
    """
    if country is None:
        response = address_controller.get_addresses(db)
    else:
        response = address_controller.get_address_by_country(db, country)

    return response


@router.get(
    path="/{id_address}",
    status_code=status.HTTP_200_OK,
    response_model=AddressResponse,
    summary="Get an address via its ID"
)
async def get_address(
        id_address: int = Path(..., gt=0),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> AddressResponse:
    """
    GET an address with specific ID

    **Path Parameter**
    -id_address(int): Field that specify the address to be retrieved

    **Query Parameter**
    - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

    **Response**
    - Return a response body of type \'AddressResponse\' with status code 200
    """
    response = address_controller.get_address_by_id(db, id_address)

    return response


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=AddressResponse,
    summary="Create an Address"
)
async def create_address(
        address_schema: AddressRequest = Body(...),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> AddressResponse:
    """
        POST an address using the request body sent by the customer

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Body Parameter**
        - The structure of the body parameter correspond to \'AddressRequest\' schema

        **Response**
        - Return a response body of type \'AddressResponse\' with status code 201
    """
    response = address_controller.create_address(db, address_schema)

    return response


@router.post(
    path="/user-batch",
    status_code=status.HTTP_201_CREATED,
    response_model=AddressResponseUser,
    summary="Create an Address with users who lived there"
)
async def create_address_with_users(
        address_schema: AddressRequestUsers = Body(...),
        test: bool = Query(False)
) -> AddressResponseUser:
    """
        POST an address with users who lived there, using the request body sent by the customer

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Body Parameter**
        - The structure of the body parameter correspond to \'AddressRequestUsers\' schema

        **Response**
        - Return a response body of type \'AddressResponseUser\' with status code 201
    """
    pass


@router.patch(
    path="/{id_address}",
    status_code=status.HTTP_200_OK,
    response_model=AddressResponse,
    summary="Update address\'s data"
)
async def update_address(
        id_address: int = Path(..., gt=0),
        address_schema: AddressRequest = Body(...),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> AddressResponse:
    """
        PATCH an address in order to update its data

        **Path Parameter**
        - id_address(int): Field that specify the address to be updated

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Body Parameter**
        - The structure of the body parameter correspond to \'AddressRequest\' schema

        **Response**
        - Return a response body of type \'AddressResponse\' with status code 200
    """
    response = address_controller.update_address(db, id_address, address_schema)

    return response


@router.put(
    path="/{id_address}/user/{id_user}",
    status_code=status.HTTP_201_CREATED,
    response_model=BasicResponse,
    summary="Assign user to address"
)
async def assign_user_to_address(
        id_address: int = Path(..., gt=0),
        id_user: int = Path(..., gt=0),
        test: bool = Query(False)
) -> BasicResponse:
    """
        PUT a user into an address

        **Path Parameter**
        - id_address(int): Field that specify the target address
        - id_user(int): Field that specify the user which will be assigned into the target address

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Response**
        - Return a response body of type \'BasicResponse\' with status code 201
    """
    pass


@router.delete(
    path="/{id_address}",
    status_code=status.HTTP_200_OK,
    response_model=BasicResponse,
    summary="Delete a specific address"
)
async def delete_address(
        id_address: int = Path(..., gt=0),
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> BasicResponse:
    """
        DELETE the address with specific ID

        **Path parameter**
        - id_address(int): Field that specify the address to be deleted

        **Query Parameter**
        - test(bool): If test is True, the system fetch data into Test DataBase, in other case,
        data is from Main Database

        **Response**
        - Return a response body of type \'BasicResponse\' with status code 200
    """
    result = address_controller.delete_address(db, id_address)

    return BasicResponse(
        operation="Delete address",
        successful=result.dropped
    )
