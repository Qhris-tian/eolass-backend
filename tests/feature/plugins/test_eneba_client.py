from typing import Dict, List

from src.plugins.eneba import EnebaClient


def test_search_product(eneba=EnebaClient()):
    response = eneba.search(product_name="call", count=1)
    assert isinstance(response, List)


def test_get_product(eneba=EnebaClient()):
    response = eneba.get_product(product_id="3cafc44d-4de4-1518-a43f-b7429be2d33c")
    assert isinstance(response, Dict)


def test_invalid_get_product(eneba=EnebaClient()):
    response = eneba.get_product(product_id="invalid-product")
    assert response is None
