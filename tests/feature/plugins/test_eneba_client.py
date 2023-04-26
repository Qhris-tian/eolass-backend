from typing import List

from src.plugins.eneba import EnebaClient


def test_search_product(eneba=EnebaClient()):
    response = eneba.search(product_name="call", count=1)
    assert isinstance(response, List)
