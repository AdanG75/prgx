import random
import string

from fastapi.testclient import TestClient

from main import app

ID_USER_TO_TEST = 0
EMAIL_USER_TO_TEST = ''


client = TestClient(app)


def test_get_users():
    response = client.get('/user/', params={"test": True})
    assert response.status_code == 200

    dropped = False
    for item in response.json():
        dropped = dropped or item["dropped"]
    assert dropped is False


def test_get_user_by_country():
    response = client.get(
        '/user/',
        params={
            "country": "Mexico",
            "test": True
        }
    )

    assert response.status_code == 200


def test_create_user():
    random_email = _random_email(20)
    response = client.post(
        '/user/',
        params={
            "test": True
        },
        json={
            "first_name": "Viridiana",
            "last_name": "Hernandez",
            "email": random_email,
            "password": "aszxqw78954"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == random_email

    global ID_USER_TO_TEST, EMAIL_USER_TO_TEST
    ID_USER_TO_TEST = response.json()["id"]
    EMAIL_USER_TO_TEST = random_email


def test_read_user():
    response = client.get(
        f'/user/{ID_USER_TO_TEST}',
        params={
            "test": True
        }
    )

    assert response.json()["id"] == ID_USER_TO_TEST
    assert response.json()["dropped"] is False


def test_update_user():
    response = client.patch(
        f'/user/{ID_USER_TO_TEST}',
        params={
            "test": True
        },
        json={
            "first_name": "Viridiana Laura",
            "last_name": "Hernandez Hernandez",
            "email": EMAIL_USER_TO_TEST,
            "password": "aszxqw78954"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == ID_USER_TO_TEST
    assert response.json()["first_name"] == "Viridiana Laura"
    assert response.json()["last_name"] == "Hernandez Hernandez"


def test_delete_user():
    response = client.delete(
        f'/user/{ID_USER_TO_TEST}',
        params={
            "test": True
        }
    )

    assert response.status_code == 200
    assert response.json()["successful"] is True


def test_assign_address_to_user():
    response_address = client.post(
        '/address/',
        params={
            "test": True
        },
        json={
            "address_1": "Calle Normal",
            "address_2": "#5",
            "city": "Guadalajara",
            "state": "Jalisco",
            "zip_code": "01236",
            "country": "Mexico"
        }
    )

    assert response_address.status_code == 201

    random_email = _random_email(20)
    response_user = client.post(
        '/user/',
        params={
            "test": True
        },
        json={
            "first_name": "Carlos",
            "last_name": "Tercero",
            "email": random_email,
            "password": "aszxqw78954"
        }
    )

    assert response_user.status_code == 201

    response_relationship = client.put(
        f'/user/{response_user.json()["id"]}/address/{response_address.json()["id"]}',
        params={
            "test": True
        }
    )

    assert response_relationship.status_code == 201
    assert response_relationship.json()["successful"] is True


def test_create_user_with_addresses():
    random_email = _random_email(24)
    response = client.post(
        "/user/address-batch",
        params={
            "test": True
        },
        json={
            "first_name": "Selena",
            "last_name": "Gomez",
            "email": random_email,
            "password": "Iamfakenews",
            "addresses": [
                {
                    "address_1": "Manzana",
                    "address_2": "9",
                    "city": "Iztacalco",
                    "state": "Ciudad de Mexico",
                    "zip_code": "32005",
                    "country": "Mexico"
                },
                {
                    "address_1": "Sierra",
                    "address_2": "8",
                    "city": "Oaxaca",
                    "state": "Oaxaca",
                    "zip_code": "451239",
                    "country": "Mexico"
                }
            ]
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == random_email
    assert len(response.json()["addresses"]) == 2


def _random_email(length):
    letters = string.ascii_lowercase + string.digits
    first_part = ''.join(random.choice(letters) for i in range(length))

    return f"{first_part}@mail.com"
