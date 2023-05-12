from fastapi import status


def test_can_get_account_balance(test_app):
    response = test_app.get("api/v1/account/balance")

    assert response.status_code == status.HTTP_200_OK
