class EnebaClient:
    """Mock http client to make enaba calls"""

    def search(self, product_name: str, count: int = 5):
        return self.dummy_products * count

    def get_product(self, product_id: str):
        product = [
            product for product in self.dummy_products if product["id"] == product_id
        ]

        if product:
            return product[0]
        return None

    dummy_products = [
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
    ]
