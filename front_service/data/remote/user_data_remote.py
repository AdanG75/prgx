from typing import List

import requests

from core.app_constants import BASE_URL
from data.remote.remote_utils import evaluate_response


def get_users(test: bool = False) -> List[dict]:
    response = requests.get(
        f"{BASE_URL}user/",
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def get_users_by_country(country: str, test: bool = False) -> List[dict]:
    response = requests.get(
        f"{BASE_URL}user/",
        params={
            "country": country,
            "test": test
        }
    )

    return evaluate_response(response)


def get_user_by_id(id_user: int, test: bool = False) -> dict:
    response = requests.get(
        f"{BASE_URL}user/{id_user}",
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def create_user(user: dict, test: bool = False) -> dict:
    response = requests.post(
        f"{BASE_URL}user/",
        json=user,
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def update_user(id_user: int, user: dict, test: bool = False) -> dict:
    response = requests.patch(
        f"{BASE_URL}user/{id_user}",
        json=user,
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def delete_user(id_user: int, test: bool = False) -> dict:
    response = requests.delete(
        f"{BASE_URL}user/{id_user}",
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def create_user_with_addresses(user: dict, test: bool = False) -> dict:
    response = requests.post(
        f"{BASE_URL}user/address-batch",
        json=user,
        params={
            "test": test
        }
    )

    return evaluate_response(response)


def assign_address_to_user(id_user: int, id_address: int, test: bool = False) -> dict:
    response = requests.put(
        f"{BASE_URL}user/{id_user}/address/{id_address}",
        params={
            "test": test
        }
    )

    return evaluate_response(response)
