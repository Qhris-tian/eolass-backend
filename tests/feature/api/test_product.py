from typing import List

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
