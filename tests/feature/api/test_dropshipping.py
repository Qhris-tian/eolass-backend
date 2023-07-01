from typing import List


def test_can_reserve_key_with_no_known_inventory(test_app):
    order_id = "67d7221c-1839-11ee-b95b-72483fd869ad"

    auction = test_app.post(
        "/api/v1/auctions?type=plain&inventory_id=5629",
        json={
            "productId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "enabled": "true",
            "keys": ["key-1"],
            "autoRenew": "true",
            "price": {"amount": 0, "currency": "string"},
            "onHand": 1,
            "declaredStock": 0,
        },
    ).json()

    response = test_app.post(
        "/api/v1/dropship/reserve",
        json={
            "action": "RESERVE",
            "orderId": order_id,
            "originalOrderId": None,
            "auctions": [
                {
                    "auctionId": auction["response"]["data"]["S_createAuction"][
                        "actionId"
                    ],
                    "keyCount": 2,
                    "price": 23,
                }
            ],
        },
    )

    response_json = response.json()

    assert response_json["action"] == "RESERVE"
    assert response_json["orderId"] == order_id
    assert response_json["success"] is False


def test_can_reserve_key_with_order_unavailable(test_app):
    order_id = "67d7221c-1839-11ee-b95b-72483fd869ad"
    test_app.post(
        "/api/v1/inventory/",
        json={"sku": 5621, "title": "random", "region": "France", "price": 98},
    ).json()

    # create eneba auction to create local auction
    auction = test_app.post(
        "/api/v1/auctions?type=plain&inventory_id=5621",
        json={
            "productId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "enabled": "true",
            "keys": ["key-1"],
            "autoRenew": "true",
            "price": {"amount": 0, "currency": "string"},
            "onHand": 1,
            "declaredStock": 0,
        },
    ).json()

    response = test_app.post(
        "/api/v1/dropship/reserve",
        json={
            "action": "RESERVE",
            "orderId": order_id,
            "originalOrderId": None,
            "available": False,
            "auctions": [
                {
                    "auctionId": auction["response"]["data"]["S_createAuction"][
                        "actionId"
                    ],
                    "keyCount": 2,
                    "price": 23,
                }
            ],
        },
    )

    response_json = response.json()

    assert response_json["action"] == "RESERVE"
    assert response_json["orderId"] == order_id
    assert response_json["success"] is False


def test_can_reserve_key(test_app):
    order_id = "67d7221c-1839-11ee-b95b-72483fd869ad"
    test_app.post(
        "/api/v1/inventory/",
        json={"sku": 5621, "title": "random", "region": "France", "price": 98},
    ).json()

    # create eneba auction to create local auction
    auction = test_app.post(
        "/api/v1/auctions?type=plain&inventory_id=5621",
        json={
            "productId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "enabled": "true",
            "keys": ["key-1"],
            "autoRenew": "true",
            "price": {"amount": 0, "currency": "string"},
            "onHand": 1,
            "declaredStock": 0,
        },
    ).json()

    response = test_app.post(
        "/api/v1/dropship/reserve",
        json={
            "action": "RESERVE",
            "orderId": order_id,
            "originalOrderId": None,
            "auctions": [
                {
                    "auctionId": auction["response"]["data"]["S_createAuction"][
                        "actionId"
                    ],
                    "keyCount": 2,
                    "price": 23,
                }
            ],
        },
    )

    response_json = response.json()

    assert response_json["action"] == "RESERVE"
    assert response_json["orderId"] == order_id
    assert response_json["success"] is True


def test_can_provision_key(test_app):
    order_id = "67d7221c-1839-11ee-b95b-72483fd869ad"

    response = test_app.post(
        "/api/v1/dropship/provision",
        json={
            "action": "PROVIDE",
            "orderId": order_id,
            "originalOrderId": None,
        },
    )

    response_json = response.json()

    assert response_json["action"] == "PROVIDE"
    assert response_json["orderId"] == order_id
    assert response_json["success"] is True
    assert isinstance(response_json["auctions"], List)
