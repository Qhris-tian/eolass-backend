from typing import List

from fastapi import status

base_endpoint = "/api/v1/inventory"


def test_can_get_inventory(test_app):
    response = test_app.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_search_requires_product_name(test_app):
    response = test_app.get(f"{base_endpoint}/search")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_can_search_inventory_with_name(test_app):
    response = test_app.get(f"{base_endpoint}/search?name=dummy_product")
    assert response.status_code == status.HTTP_200_OK


def test_can_inventory_cards(test_app):
    response = test_app.get(f"{base_endpoint}/12/cards")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
