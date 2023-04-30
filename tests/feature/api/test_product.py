from typing import Dict, List

from fastapi import status


def test_search_product_requires_product_name(test_app):
    response = test_app.get("/api/v1/products/search")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["errors"] == {"product": "field required"}


def test_search_product_returns_200_with_product_name(test_app):
    response = test_app.get(
        "/api/v1/products/search?product={product}".format(product="call")
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["products"], List)


def test_get_product_details_with_id_returns_200_for_valid_id(test_app):
    response = test_app.get(
        "/api/v1/products/{id}".format(id="3cafc44d-4de4-1518-a43f-b7429be2d33c")
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), Dict)


def test_get_product_details_with_id_returns_404_for_invalid_id(test_app):
    response = test_app.get("/api/v1/products/invalid-id")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["errors"] == ["Product does not exist."]
