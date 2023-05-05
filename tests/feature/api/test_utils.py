from src.api_v1.auction import utils
from tests.mocks.schema import CreateAuctionMock, UpdateAuctionMock


def test_get_create_auction_preorder():
    data = utils.get_create_auction_preorder(CreateAuctionMock)
    assert "query" in data


def test_get_create_auction_declared_stock():
    data = utils.get_create_auction_declared_stock(CreateAuctionMock)
    assert "query" in data


def test_get_update_auction_declared_stock():
    data = utils.get_update_auction_declared_stock(UpdateAuctionMock)
    assert "query" in data


def test_get_update_auction_plain():
    data = utils.get_update_auction_plain(UpdateAuctionMock)
    assert "query" in data


def test_get_create_auction_query():
    data_plain = utils.get_create_auction_query(CreateAuctionMock, type="plain")
    assert "query" in data_plain

    data_preorder = utils.get_create_auction_query(CreateAuctionMock, type="preorder")
    assert "query" in data_preorder

    data_declared_stock = utils.get_create_auction_query(
        CreateAuctionMock, type="declaredstock"
    )
    assert "query" in data_declared_stock

    data_default = utils.get_create_auction_query(CreateAuctionMock, type="")
    assert data_default == ""


def test_get_update_auction_query():
    data_plain = utils.get_update_auction_query(UpdateAuctionMock, type="plain")
    assert "query" in data_plain

    data_declared_stock = utils.get_update_auction_query(
        UpdateAuctionMock, type="declaredstock"
    )
    assert "query" in data_declared_stock

    data_default = utils.get_update_auction_query(UpdateAuctionMock, type="")
    assert data_default == ""


def test_get_enable_declared_stock_query():
    data = utils.get_enable_declared_stock_query()
    assert "query" in data

def test_get_fee_query():
    data = utils.get_fee_query(currency="EUR", type="AUCTION_NEW")
    assert "query" in data
