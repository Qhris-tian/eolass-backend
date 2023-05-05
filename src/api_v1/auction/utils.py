import json

from .schema import CreateAuctionRequest, UpdateAuctionRequest


def get_create_auction_plain(body: CreateAuctionRequest):
    return {
        "query": """
            mutation {
                S_createAuction(
                    input: {
                    productId: "%s"
                    enabled: %s
                    keys: %s
                    autoRenew: %s
                    price: { amount: %s, currency: "%s" }
                    }
                ) {
                    isSuccessful
                    actionId
                }
                }
            """
        % (
            body.productId,
            body.enabled,
            json.dumps(body.keys),
            body.autoRenew,
            body.price.amount,
            body.price.currency,
        )
    }


def get_create_auction_preorder(body: CreateAuctionRequest):
    return {
        "query": """
                mutation {
                    S_createAuction(
                        input: {
                        productId: "%s"
                        enabled: %s
                        keys: %s
                        onHand: %s
                        autoRenew: %s
                        price: { amount: %s, currency: "%s" }
                        }
                    ) {
                        isSuccessful
                        actionId
                    }
                }
            """
        % (
            body.productId,
            body.enabled,
            json.dumps(body.keys),
            body.onHand,
            body.autoRenew,
            body.price.amount,
            body.price.currency,
        )
    }


def get_create_auction_declared_stock(body: CreateAuctionRequest):
    return {
        "query": """
            mutation {
                S_createAuction(
                    input: {
                    productId: "%s"
                    enabled: %s
                    declaredStock: %s
                    autoRenew: %s
                    price: { amount: %s, currency: "%s" }
                    }
                ) {
                    isSuccessful
                    actionId
                }
                }
            """
        % (
            body.productId,
            body.enabled,
            body.declaredStock,
            body.autoRenew,
            body.price.amount,
            body.price.currency,
        )
    }


def get_update_auction_plain(body: UpdateAuctionRequest):
    return {
        "query": """
        mutation {
            S_updateAuction(
                input: {
                id: "%s"
                addedKeys: %s
                removedKeys: %s
                price: { amount: %s, currency: "%s" }
                }
            ) {
                isSuccessful
                actionId
            }
            }
        """
        % (
            body.id,
            json.dumps(body.addedKeys),
            json.dumps(body.removedKeys),
            body.price.amount,
            body.price.currency,
        )
    }


def get_update_auction_declared_stock(body: UpdateAuctionRequest):
    return {
        "query": """
            mutation {
            S_updateAuction(
                input: {
                id: "%s"
                declaredStock: %s
                }
            ) {
                isSuccessful
                actionId
            }
            }
        """
        % (body.id, body.declaredStock)
    }


def get_create_auction_query(data: CreateAuctionRequest, type):
    match type:
        case "plain":
            return get_create_auction_plain(data)
        case "preorder":
            return get_create_auction_preorder(data)
        case "declaredstock":
            return get_create_auction_declared_stock(data)
        case _:
            return ""


def get_update_auction_query(data: UpdateAuctionRequest, type):
    match type:
        case "plain":
            return get_update_auction_plain(data)
        case "declaredstock":
            return get_update_auction_declared_stock(data)
        case _:
            return ""


def get_enable_declared_stock_query():
    return {
        "query": """
            mutation {
                P_enableDeclaredStock {
                    success
                    failureReason
                }
            }
        """
    }


def get_keys_query(stock_id):
    return {
        "query": """
            {
                S_keys(stockId: "%s") {
                    edges {
                    node {
                        id
                        value
                        state
                    }
                    }
                }
            }
        """
        % (stock_id)
    }


def get_fee_query(currency, type):
    return {
        "query": """
            {
                T_countFee(currency: "%s", type: %s) {
                    fee {
                    amount
                    currency
                    }
                }
            }
        """
        % (currency, type)
    }
