import random
import string
from datetime import datetime
from typing import Dict
from uuid import uuid4


class Ezpin:
    """Mock http client to fake ezpin calls"""

    def get_order_history(
        self, start_date: datetime, end_date: datetime, limit: int = 10, offset: int = 0
    ):
        return {
            "count": limit,
            "next": "",
            "previous": "",
            "results": [
                {
                    **dummy_order,
                    "reference_code": str(uuid4()),
                    "count": (i % 5) + 1,
                    "status_text": "accept" if i % 3 else "pending",
                }
                for i in range(limit)
            ],
        }

    def get_order(self, reference_code: str):
        return {**dummy_order, "reference_code": reference_code}

    def get_order_cards(self, reference_code):
        return [dummy_order_card]

    def create_order(self, data: Dict):
        return {**dummy_order, "reference_code": data["reference_code"]}

    def catalog_list(self):
        return {
            "count": 5,
            "next": "dummy_next_url",
            "previous": "dummy_previous_url",
            "results": [dummy_product for i in range(5)],
        }

    def catalog_availability(self, product_id: str, data: Dict):
        available = True if random.randint(0, 1) else False
        detail = (
            "This catalog is available."
            if available
            else "This catalog is not available."
        )

        return {"availability": available, "detail": detail}


dummy_order = {
    "order_id": 156734,
    "delivery_type": 3,
    "destination": "18004441234",
    "status": 1,
    "status_text": "accept",
    "created_time": "2021-09-19T12:46:19.577169",
    "terminal_id": 97,
    "reference_code": "bb715b4e-6792-45ca-9ca5-2d708f41a6e0",
    "product": {"sku": random.randint(1001, 9999), "title": "App Store & iTunes US"},
    "count": 1,
    "total_face_value": 3.0,
    "total_fees": 0,
    "total_discounts": 0.42,
    "total_customer_cost": 3.42,
    "is_completed": True,
    "share_link": "http://vc.ezpaypin.com/01c79b97-8ab4-423c-a11d-225897f2135a",
}

dummy_product = {
    "sku": 562,
    "upc": 659245724761,
    "title": "Amazon DE",
    "min_price": 19.99,
    "max_price": 19.99,
    "pre_order": False,
    "activation_fee": 0.0,
    "percentage_of_buying_price": 20.0,
    "currency": {"currency": "Dollars", "symbol": "$", "code": "USD"},
    "categories": [{"name": "CALL OF DUTY"}, {"name": "CALL OF DUTY"}],
    "regions": [{"name": "Global", "code": "GLC"}],
    "image": "https://media.ezpaypin.com/media/products/images/2020/09/amazon.jpg",
    "description": "",
    "showing_price": {
        "price": 35.0,
        "showing_currency": {"currency": "Lira", "symbol": "TL", "code": "TRY"},
    },
}


dummy_order_card = {
    "card_number": "".join((random.choice(string.ascii_uppercase) for x in range(9))),
    "pin_code": "393145478240831916",
    "claim_url": "https://vc.ezpaypin.com/9853476c-3b05-4871-a56f-9bb7eb33891d",
    "expire_date": "",
}
