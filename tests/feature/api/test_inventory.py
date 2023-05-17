import random
from typing import Dict, List

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
    sku = random.randint(1001, 2009)

    test_app.post(
        f"{base_endpoint}/",
        json={
            "sku": sku,
            "title": "random",
        },
    )

    response = test_app.post(
        "{b}/{sku}/cards".format(b=base_endpoint, sku=sku),
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


def test_can_create_inventory(test_app):
    sku = random.randint(1001, 2009)

    response = test_app.post(
        f"{base_endpoint}/",
        json={
            "sku": sku,
            "title": "random",
            "region": "France",
        },
    )

    inventory = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(inventory, Dict)
    assert inventory["sku"] == sku


def test_can_pseudo_create_existing_inventory(test_app):
    sku = random.randint(1001, 2009)

    test_app.post(
        f"{base_endpoint}/",
        json={
            "sku": sku,
            "title": "Jump",
        },
    )

    response = test_app.post(
        f"{base_endpoint}/",
        json={
            "sku": sku,
            "title": "Street",
        },
    )

    inventory = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(inventory, Dict)
    assert inventory["sku"] == sku
    assert inventory["title"] == "Street"


def test_can_update_existing_inventory(test_app):
    sku = random.randint(1001, 2009)

    test_app.post(f"{base_endpoint}", json={"sku": sku, "title": "Jump"})
    response = test_app.put(
        f"{base_endpoint}/{sku}", json={"sku": sku, "title": "Street"}
    )

    assert response.status_code == status.HTTP_200_OK


def test_cannot_update_non_existing_inventory(test_app):
    response = test_app.put(f"{base_endpoint}/{1}", json={"sku": 1, "title": "Street"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
