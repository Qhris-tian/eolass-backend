from typing import Dict, List

from src.plugins.eneba import EnebaClient
from src.api_v1.transaction.schema import TransactionTypeEnum
from tests.mocks.schema import CreateAuctionMock, UpdateAuctionMock


def test_search_product(eneba=EnebaClient()):
    response = eneba.search(product_name="call", count=1)
    assert isinstance(response, List)


def test_get_auctions(eneba=EnebaClient()):
    response = eneba.get_auctions(limit=1, page=None)
    assert "edges" in response


def test_create_auction(eneba=EnebaClient()):
    response = eneba.create_auction(body=CreateAuctionMock, type="plain")
    assert "data" in response


def test_update_auction(eneba=EnebaClient()):
    response = eneba.update_auction(body=UpdateAuctionMock, type="plain")
    assert "data" in response


# def test_enable_declared_stock(eneba=EnebaClient()):
#     respone = eneba.enable_declared_stock()
#     assert "data" in respone


def test_get_keys(eneba=EnebaClient()):
    response = eneba.get_keys(stock_id="61077c78-e5ff-11ed-8cac-c2d0bec86bc4", limit=2)
    assert "data" in response


def test_get_product(eneba=EnebaClient()):
    response = eneba.get_product(product_id="3cafc44d-4de4-1518-a43f-b7429be2d33c")
    assert isinstance(response, Dict)


def test_invalid_get_product(eneba=EnebaClient()):
    response = eneba.get_product(product_id="invalid-product")
    assert response is None


def test_get_fee(eneba=EnebaClient()):
    response = eneba.get_fee(currency="EUR", type="AUCTION_NEW")
    assert "data" in response


def test_get_transactions(eneba=EnebaClient()):
    response = eneba.get_transactions(type= TransactionTypeEnum.sale)
    assert "data" in response
