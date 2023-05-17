from fastapi import status


def test_get_transactions(test_app):
    response = test_app.get("/api/v1/transactions")

    assert response.status_code == status.HTTP_200_OK
    assert "response" in response.json()
