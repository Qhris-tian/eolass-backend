
from .schema import CreateAuctionRequest
import json

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
            %(body.productId, body.enabled, json.dumps(body.keys), body.autoRenew, body.price.amount, body.price.currency)
        }

def get_create_auction_preorder(body: CreateAuctionRequest):

    return {
            "query": """
                mutation {
                    S_createAuction(
                        input: {
                        productId: "%s"
                        enabled: %s
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
            %(body.productId, body.enabled, body.onHand, body.autoRenew, body.price.amount, body.price.currency)
        }

    # return {
    #     "query": """
    #         mutation {
    #             S_createAuction(
    #                 input: {
    #                 productId: "92c73bdc-80d4-1041-a4de-c12cc3d288c0"
    #                 enabled: true
    #                 onHand: 50
    #                 autoRenew: false
    #                 price: { amount: 1399, currency: "EUR" }
    #                 }
    #             ) {
    #                 isSuccessful
    #                 actionId
    #             }
    #             }
    #     """
    # }

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
            %(body.productId, body.enabled, body.declaredStock, body.autoRenew, body.price.amount, body.price.currency)
        }

def get_create_auction_query(data: CreateAuctionRequest):
    match data.type:
        case "plain":
            return get_create_auction_plain(data)
        case "preorder":
            return get_create_auction_preorder(data)
        case "declaredstock":
            return get_create_auction_declared_stock(data)
        case default:
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
        %(stock_id)
    }