from fastapi.testclient import TestClient

from main import app
from tests.test_user_router import _random_email

ID_ADDRESS_TO_TEST = 0


client = TestClient(app)


def test_get_address():
    response = client.get('/address/', params={"test": True})
    assert response.status_code == 200

    dropped = False
    for item in response.json():
        dropped = dropped or item["dropped"]
    assert dropped is False


def test_get_address_by_country():
    response = client.get(
        '/address/',
        params={
            "country": "Mexico",
            "test": True
        }
    )

    assert response.status_code == 200

    same_country = True
    for address in response.json():
        same_country = same_country and (address["country"] == "Mexico")

    assert same_country is True


def test_create_address():
    response = client.post(
        '/address/',
        params={
            "test": True
        },
        json={
            "address_1": "Main Street",
            "address_2": "#89-A",
            "city": "Huston",
            "state": "Texas",
            "zip_code": "555555",
            "country": "United States"
        }
    )

    assert response.status_code == 201
    assert response.json()["address_1"] == "Main Street"
    assert response.json()["address_2"] == "#89-A"
    assert response.json()["city"] == "Huston"
    assert response.json()["state"] == "Texas"
    assert response.json()["zip_code"] == "555555"
    assert response.json()["country"] == "United States"

    global ID_ADDRESS_TO_TEST
    ID_ADDRESS_TO_TEST = response.json()["id"]


def test_read_address():
    response = client.get(
        f'/address/{ID_ADDRESS_TO_TEST}',
        params={
            "test": True
        }
    )

    assert response.json()["id"] == ID_ADDRESS_TO_TEST
    assert response.json()["dropped"] is False


def test_update_address():
    response = client.patch(
        f'/address/{ID_ADDRESS_TO_TEST}',
        params={
            "test": True
        },
        json={
            "address_1": "Main Street",
            "address_2": "#89-A 2° floor",
            "city": "Huston",
            "state": "Texas",
            "zip_code": "555554",
            "country": "United States"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == ID_ADDRESS_TO_TEST
    assert response.json()["address_2"] == "#89-A 2° floor"
    assert response.json()["zip_code"] == "555554"


def test_delete_address():
    response = client.delete(
        f'/address/{ID_ADDRESS_TO_TEST}',
        params={
            "test": True
        }
    )

    assert response.status_code == 200
    assert response.json()["successful"] is True


def test_assign_user_to_address():
    response_address = client.post(
        '/address/',
        params={
            "test": True
        },
        json={
            "address_1": "Calle Excelencia",
            "address_2": "#25",
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
            "first_name": "Maximiliano",
            "last_name": "Bermudez",
            "email": random_email,
            "password": "aszxqw78954"
        }
    )

    assert response_user.status_code == 201

    response_relationship = client.put(
        f'/address/{response_address.json()["id"]}/user/{response_user.json()["id"]}',
        params={
            "test": True
        }
    )

    assert response_relationship.status_code == 201
    assert response_relationship.json()["successful"] is True


def test_create_address_with_users():
    response = client.post(
        "/address/user-batch",
        params={
            "test": True
        },
        json={
            "address_1": "Callejon",
            "address_2": "2",
            "city": "Bogota",
            "state": "Bogota",
            "zip_code": "94102",
            "country": "Colombia",
            "users": [
                {
                    "first_name": "Pedro",
                    "last_name": "Infante",
                    "email": _random_email(24),
                    "password": "IamNotDead"
                },
                {
                    "first_name": "Elvis",
                    "last_name": "Presly",
                    "email": _random_email(24),
                    "password": "IamNotDeadx2"
                }
            ]
        }
    )

    assert response.status_code == 201
    assert response.json()["address_1"] == "Callejon"
    assert response.json()["address_2"] == "2"
    assert response.json()["city"] == "Bogota"
    assert response.json()["state"] == "Bogota"
    assert response.json()["zip_code"] == "94102"
    assert response.json()["country"] == "Colombia"
    assert len(response.json()["users"]) == 2

