from typing import List

from src.plugins.eneba import EnebaClient
from tests.mocks.schema import CreateAuctionMock


def test_search_product(eneba=EnebaClient()):
    response = eneba.search(product_name="call", count=1)
    assert isinstance(response, List)

def test_get_auctions(eneba=EnebaClient()):
    response = eneba.get_auctions(limit=1)
    assert "edges" in response

def test_create_auction(eneba=EnebaClient()):
    response = eneba.create_auction(body=CreateAuctionMock, type="plain")
    assert "data" in response