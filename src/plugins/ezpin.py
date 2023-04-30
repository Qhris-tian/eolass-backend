from datetime import datetime
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

    def get_order_history(
        self, start_date: datetime, end_date: datetime, limit: int = 10, offset: int = 0
    ):
        return self.get("orders/")

    def get_order(self, reference_code):
        return self.get(f"orders/{reference_code}")

    def get_order_cards(self, reference_code: UUID):
        return self.get(f"orders/{reference_code}/cards")

    def create_order(self, data: Dict):
        return self.post_json(
            "orders/",
            data={
                "product_id": data["product_id"],
                "item_count": data["quantity"],
                "price": data["price"],
            },
        )

    def catalog_list(self):
        return self.get("catalogs/")

    def catalog_availability(self, product_id: str, data: Dict):
        return self.get(
            f"catalogs/{product_id}/availability/",
            params=data,
        )


@timed_lru_cache(36000)
def get_access_token() -> str:  # pragma: no cover
    response = requests.post(
        "{}/{}".format(settings.ENEBA_BASE_URI, "auth/token"),
        data={
            "id": settings.ENEBA_ID,
            "secret_key": settings.ENEBA_SECRET,
        },
    ).json()

    return response.get("access_token")
