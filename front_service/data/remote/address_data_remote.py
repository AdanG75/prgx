from typing import List

import requests

from core.app_constants import BASE_URL
from data.remote.remote_utils import evaluate_response


def get_addresses(test: bool = False) -> List[dict]:
    response = requests.get(
        f"{BASE_URL}address/",
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def get_addresses_by_country(country: str, test: bool = False) -> List[dict]:
    response = requests.get(
        f"{BASE_URL}address/",
        params={
            "country": country,
            "test": test
        }
    )

    return evaluate_response(response)


def get_address_by_id(id_address: int, test: bool = False) -> dict:
    response = requests.get(
        f"{BASE_URL}address/{id_address}",
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def create_address(address: dict, test: bool = False) -> dict:
    response = requests.post(
        f"{BASE_URL}address/",
        json=address,
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def update_address(id_address: int, address: dict, test: bool = False) -> dict:
    response = requests.patch(
        f"{BASE_URL}address/{id_address}",
        json=address,
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def delete_address(id_address: int, test: bool = False) -> dict:
    response = requests.delete(
        f"{BASE_URL}address/{id_address}",
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def create_address_with_users(address: dict, test: bool = False) -> dict:
    response = requests.post(
        f"{BASE_URL}address/user-batch",
        json=address,
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def assign_user_to_address(id_address: int, id_user: int, test: bool = False) -> dict:
    response = requests.put(
        f"{BASE_URL}address/{id_address}/user/{id_user}",
        params={
            "test": test
        }
    )

    return evaluate_response(response)
