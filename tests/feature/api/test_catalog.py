from typing import List, Dict

from fastapi import status


def test_can_get_catalog_history(test_app):
    response = test_app.get("/api/v1/catalogs")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), Dict)
    assert isinstance(response.json()["results"], List)


def test_price_and_quantity_must_be_greater_than_zero(test_app):
    response = test_app.get("/api/v1/catalogs/product/availability?price=0&quantity=0")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response.json(), Dict)


def test_can_check_catalog_availability(test_app):
    response = test_app.get("/api/v1/catalogs/product/availability?price=1&quantity=1")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), Dict)
