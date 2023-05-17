from fastapi import status

base_endpoint = "/api/v1/cards"


def test_can_get_cards(test_app):
    response = test_app.get(base_endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_can_get_only_avialable_cards(test_app):
    response = test_app.get(f"{base_endpoint}?available={True}")
    assert response.status_code == status.HTTP_200_OK


def test_can_get_only_unavailable_cards(test_app):
    response = test_app.get(f"{base_endpoint}?available={False}")
    assert response.status_code == status.HTTP_200_OK
