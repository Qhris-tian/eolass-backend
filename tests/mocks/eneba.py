class EnebaClient:
    """Mock http client to make enaba calls"""

    def search(self, product_name: str, count: int = 5):
        return [
            {
                "id": "3cafc44d-4de4-1518-a43f-b7429be2d33c",
                "name": "Call of Duty: WWII",
                "languages": ["Afrikaans", "Chinese", "Danish"],
                "regions": [{"code": "oman"}],
                "releasedAt": "2017-11-03T00:00:00+00:00",
                "createdAt": "2017-11-03T00:00:00+00:00",
                "slug": "call-of-duty-wwii",
                "type": {"value": "GAME"},
                "auctions": [
                    {
                        "belongsToYou": False,
                        "isInTtock": True,
                        "merchantName": "MGG Studio TEST",
                        "price": {"amount": 1903, "currency": "EUR"},
                    }
                ],
            }
        ] * count
    
    def get_auctions(self, limit: int = 1):
        return {
            "edges": [
            {
                "node": {
                "id": "61077c78-e5ff-11ed-8cac-c2d0bec86bc4",
                "product": {
                    "id": "92c73bdc-80d4-1041-a4de-c12cc3d288c0",
                    "name": "Half Life 3"
                },
                "unitsSold": 0,
                "onHold": 0,
                "onHand": 2,
                "declaredStock": 'null',
                "status": "ACTIVE",
                "expiresAt": "2021-01-01T00:00:00+00:00",
                "createdAt": "2023-04-28T20:00:52+00:00",
                "autoRenew": 'false',
                "price": {
                    "amount": 1399,
                    "currency": "EUR"
                },
                "position": 15,
                "priceUpdateQuota": {
                    "quota": 100,
                    "nextFreeIn": 'null',
                    "totalFree": 100
                }
                }
            }
            ] * limit
        }
    
