from datetime import date
from typing import Dict
from uuid import UUID

import requests

from src.config import get_settings
from src.decorators import timed_lru_cache

from .base_client import BaseClient

settings = get_settings()


class Ezpin(BaseClient):  # pragma: no cover
    def __init__(
        self,
    ):
        token = get_access_token()
        self.timeout = 60
        super().__init__(settings.EZPIN_BASE_URI, token=token)

    def get_account_balance(self):
        return self.get("balance/").json()

    def get_order_history(
        self, start_date: date, end_date: date, limit: int = 10, offset: int = 0
    ):
        return self.get(
            "orders/",
            {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "limit": limit,
                "offset": offset,
            },
        ).json()

    def get_order(self, reference_code):
        return self.get(f"orders/{reference_code}/").json()

    def get_order_cards(self, reference_code: UUID):
        return self.get(f"orders/{reference_code}/cards/").json()

    def create_order(self, data: Dict):
        return self.post_json(
            "orders/",
            data={
                "product_id": data["product_id"],
                "item_count": data["quantity"],
                "price": data["price"],
            },
        ).json()

    def catalog_list(self):
        return self.get("catalogs/").json()

    def catalog_availability(self, product_id: str, data: Dict):
        return self.get(
            f"catalogs/{product_id}/availability/",
            params=data,
        ).json()

    def crypto_catalog_list(self):  # pragma: no cover
        return self.get("crypto/catalog/").json()


@timed_lru_cache(10080)
def get_access_token() -> str:  # pragma: no cover
    response = requests.post(
        "{}/{}".format(settings.EZPIN_BASE_URI, "auth/token/"),
        json={
            "client_id": settings.EZPIN_ID,
            "secret_key": settings.EZPIN_SECRET,
        },
    ).json()

    return response.get("access")
