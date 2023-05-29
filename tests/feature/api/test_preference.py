import random
from typing import Dict, List

from fastapi import status

base_endpoint = "/api/v1/preferences"


def test_can_get_preference(test_app):
    response = test_app.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_can_create_preference(test_app):
    response = test_app.post(
        base_endpoint,
        json={
            "spending_limits": [{"interval": "DAILY", "value": 80000}],
            "auction_percentage_selling_price": 0.02,
        },
    )
    preference = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert preference["auction_percentage_selling_price"] == 0.02


def test_can_update_preference(test_app):
    response = test_app.post(
        base_endpoint,
        json={
            "spending_limits": [{"interval": "DAILY", "value": 80000}],
            "auction_percentage_selling_price": 0.02,
        },
    )
    preference = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert preference["auction_percentage_selling_price"] == 0.02

    response = test_app.put(
        f"{base_endpoint}/{preference['_id']}",
        json={
            "spending_limits": [{"interval": "DAILY", "value": 80000}],
            "auction_percentage_selling_price": 0.01,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    update = response.json()

    assert update["auction_percentage_selling_price"] == 0.01
