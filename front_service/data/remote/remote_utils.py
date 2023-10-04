from typing import Union, List

from fastapi import status

from requests import Response

from data.remote.remote_exceptions import NOT_FOUND, SERVER_ERROR, BAD_DATA


def evaluate_response(response: Response) -> Union[dict, List[dict]]:
    if response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_201_CREATED:
        return response.json()
    elif (response.status_code == status.HTTP_400_BAD_REQUEST or
          response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY):
        raise BAD_DATA
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        raise NOT_FOUND
    else:
        raise SERVER_ERROR
