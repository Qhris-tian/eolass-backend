from datetime import date
from typing import Dict, List
from urllib.parse import urlencode
from uuid import uuid4

from fastapi import status

base_endpoint = "/api/v1/orders"
preference_endpoint = "/api/v1/preferences"


def test_cannot_create_order_when_price_or_quantity_is_less_than_zero(test_app):
    response = test_app.post(
        base_endpoint,
        json={"product_id": 12, "quantity": 0, "price": 0, "pre_order": True},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_can_create_order(test_app):
    response = test_app.post(
        base_endpoint,
        json={"product_id": 12, "quantity": 12, "price": 2.3, "pre_order": True},
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_can_get_order_history_without_params(test_app):
    response = test_app.get(base_endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), Dict)
    assert isinstance(response.json()["results"], List)


def test_can_get_order_history_with_only_start_date(test_app):
    params = urlencode({"start_date": date.today()})
    response = test_app.get(f"{base_endpoint}/?{params}")

    assert isinstance(response.json(), Dict)
    assert isinstance(response.json()["results"], List)

    assert response.status_code == status.HTTP_200_OK


def test_can_get_order_history_with_only_end_date(test_app):
    params = urlencode({"end_date": date.today()})

    response = test_app.get(f"{base_endpoint}/?{params}")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), Dict)
    assert isinstance(response.json()["results"], List)


def test_can_get_local_orders(test_app):
    response = test_app.get(f"{base_endpoint}/local")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)


def test_can_get_order(test_app):
    response = test_app.get("{}/{}".format(base_endpoint, str(uuid4())))

    assert response.status_code == status.HTTP_200_OK


def test_cannot_refresh_non_existing_order(test_app):
    response = test_app.get("{}/{}/refresh".format(base_endpoint, str(uuid4())))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["errors"] == ["Order not found"]


def test_can_refresh_existing_order(test_app):
    create_response = test_app.post(
        base_endpoint,
        json={"product_id": 12, "quantity": 12, "price": 2.3, "pre_order": False},
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    get_response = test_app.get(f"{base_endpoint}/local")
    assert get_response.status_code == status.HTTP_200_OK

    created_order = get_response.json()[0]

    response = test_app.get(
        "{}/{}/refresh".format(base_endpoint, created_order["reference_code"])
    )
    assert response.status_code == status.HTTP_200_OK


def test_cannot_refresh_existing_completed_order(test_app):
    response = test_app.post(
        base_endpoint,
        json={"product_id": 12, "quantity": 12, "price": 2.3, "pre_order": False},
    )
    assert response.status_code == status.HTTP_201_CREATED

    get_response = test_app.get(f"{base_endpoint}/local")
    assert get_response.status_code == status.HTTP_200_OK

    created_order = get_response.json()[0]

    response = test_app.get(
        "{}/{}/refresh".format(base_endpoint, created_order["reference_code"])
    )
    assert response.status_code == status.HTTP_200_OK

    response = test_app.get(
        "{}/{}/refresh".format(base_endpoint, created_order["reference_code"])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Order has already been completed."}


def test_cannot_create_order_when_order_limit_reached(test_app):
    response = test_app.post(
        preference_endpoint,
        json={
            "spending_limits": [{"interval": "ANNUAL", "value": 150.0}],
            "auction_percentage_selling_price": 0.02,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = test_app.post(
        base_endpoint,
        json={"product_id": 10, "quantity": 14, "price": 10, "pre_order": False},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
