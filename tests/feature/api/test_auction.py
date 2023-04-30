from fastapi import status

def test_get_auctions_endpoint(test_app):
    response = test_app.get("/api/v1/auctions/")

    assert response.status_code == status.HTTP_200_OK
    assert "auctions" in response.json()


def test_create_auction(test_app):
    response = test_app.post("/api/v1/auctions/", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_update_auction_endpoint(test_app):
    response = test_app.put("/api/v1/auctions/61077c78-e5ff-11ed-8cac-c2d0bec86bc4", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY