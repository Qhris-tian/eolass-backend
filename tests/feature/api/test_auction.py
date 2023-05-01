from fastapi import status


def test_get_auctions_endpoint(test_app):
    response = test_app.get("/api/v1/auctions/")

    assert response.status_code == status.HTTP_200_OK
    assert "auctions" in response.json()


def test_create_auction(test_app):
    create_data = {
        "productId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "enabled": "true",
        "keys": ["string"],
        "autoRenew": "true",
        "price": {"amount": 0, "currency": "string"},
        "onHand": 0,
        "declaredStock": 0,
    }
    response = test_app.post("/api/v1/auctions?type=plain", json=create_data)

    assert response.status_code == status.HTTP_200_OK
    assert "response" in response.json()


def test_update_auction_endpoint(test_app):
    update_data = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "price": {"amount": 0, "currency": "string"},
        "addedKeys": ["string"],
        "acquisitionPrice": {"amount": 0, "currency": "string"},
        "removedKeys": ["string"],
        "enabled": "false",
        "autoRenew": "false",
        "lowStockNotificationEnabled": "false",
        "priceChangeNotificationEnabled": "false",
        "declaredStock": 0,
    }
    response = test_app.put(
        "/api/v1/auctions/61077c78-e5ff-11ed-8cac-c2d0bec86bc4?type=plain",
        json=update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert "response" in response.json()


def test_get_keys(test_app):
    response = test_app.get(
        "/api/v1/auctions/keys/61077c78-e5ff-11ed-8cac-c2d0bec86bc4"
    )

    assert "edges" in response.json()["response"]
