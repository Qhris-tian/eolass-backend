from datetime import datetime
from typing import Dict

import requests

from src.config import get_settings
from src.decorators import timed_lru_cache

from .base_client import BaseClient

settings = get_settings()


class Ezpin(BaseClient):
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

    def get_order(self, order_id):
        return self.get(f"orders/{order_id}")

    def create_order(self, data=Dict):
        return self.post("orders/", data=data)

    def catalog_list(self):
        return self.get("catalogs/")

    def catalog_availability(self, product_id: str):
        return self.get(f"catalogs/{product_id}/availability/")


@timed_lru_cache(36000)
def get_access_token() -> str:
    response = requests.post(
        "{}/{}".format(settings.ENEBA_BASE_URI, "auth/token"),
        data={
            "id": settings.ENEBA_ID,
            "secret_key": settings.ENEBA_SECRET,
        },
    ).json()

    return response.get("access_token")
