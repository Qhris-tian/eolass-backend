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


def test_can_create_inventory_card(test_app):
    response = test_app.get(base_endpoint)
    inventory = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(inventory, List)

    response = test_app.post(
        "{b}/{sku}/cards".format(b=base_endpoint, sku=inventory[0]["sku"]),
        json={
            "card_number": "ASDFAFFSAD",
            "pin_code": "234124124141",
            "claim_url": None,
            "expire_date": "2023-04-02",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_cannot_create_card_for_non_existing_inventory(test_app):
    response = test_app.post(
        f"{base_endpoint}/232411313213/cards",
        json={
            "card_number": "ASDFAFFSAD",
            "pin_code": "234124124141",
            "claim_url": None,
            "expire_date": "2023-04-02",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cannot_create_card_for_invalid_inventory_sku(test_app):
    response = test_app.post(
        f"{base_endpoint}/string/cards",
        json={
            "card_number": "ASDFAFFSAD",
            "pin_code": "234124124141",
            "claim_url": None,
            "expire_date": "2023-04-02",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
