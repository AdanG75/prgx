from fastapi import APIRouter, HTTPException, status

import requests

from core.app_constants import BASE_URL

route = APIRouter(prefix="/health", tags=["Health"])


@route.get(
    path="/inner-server",
    status_code=status.HTTP_200_OK,
    summary="Check if inner-service is available"
)
async def communicate_inner_server():
    """
    GET a default response of the inner-service

    **Exceptions**
    - Raise a server error, status code 500, if it was not possible
    to connect with the service
    """
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            detail="Something went wrong",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )