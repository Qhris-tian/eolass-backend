from typing import List
from uuid import uuid4
from urllib.parse import urlencode
from datetime import datetime

from fastapi import status

base_endpoint = "/api/v1/orders"


def test_cannot_create_order_when_price_or_quantity_is_less_than_zero(test_app):
    response = test_app.post(
        base_endpoint, json={"product_id": 12, "quantity": 0, "price": 0}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_can_create_order(test_app):
    response = test_app.post(
        base_endpoint, json={"product_id": 12, "quantity": 12, "price": 2.3}
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_can_get_order_history_without_params(test_app):
    response = test_app.get(base_endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)


def test_can_get_order_history_with_only_start_date(test_app):
    params = urlencode({"start_date": datetime.now()})
    response = test_app.get(f"{base_endpoint}/?{params}")

    assert isinstance(response.json(), List)
    assert response.status_code == status.HTTP_200_OK


def test_can_get_order_history_with_only_end_date(test_app):
    params = urlencode({"end_date": datetime.now()})

    response = test_app.get(f"{base_endpoint}/?{params}")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)


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
    response = test_app.post(
        base_endpoint, json={"product_id": 12, "quantity": 12, "price": 2.3}
    )
    assert response.status_code == status.HTTP_201_CREATED

    created_order = response.json()

    response = test_app.get(
        "{}/{}/refresh".format(base_endpoint, created_order["reference_code"])
    )
    assert response.status_code == status.HTTP_200_OK

def test_cannot_refresh_existing_completed_order(test_app):
    response = test_app.post(
        base_endpoint, json={"product_id": 12, "quantity": 12, "price": 2.3}
    )
    assert response.status_code == status.HTTP_201_CREATED

    created_order = response.json()

    response = test_app.get(
        "{}/{}/refresh".format(base_endpoint, created_order["reference_code"])
    )
    assert response.status_code == status.HTTP_200_OK
    
    response = test_app.get(
        "{}/{}/refresh".format(base_endpoint, created_order["reference_code"])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Order has already been completed."}
