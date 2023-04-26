from typing import Dict, List

import requests

from src.config import get_settings
from src.decorators import timed_lru_cache
from src.plugins.base_client import BaseClient

settings = get_settings()


class EnebaClient(BaseClient):
    """Http client to make enaba calls"""

    def __init__(
        self,
    ):
        token = get_access_token()
        self.timeout = 60
        super().__init__(settings.ENEBA_BASE_URI, token=token)

    def search(self, product_name: str, count: int = 5):
        response = self.post_json(
            "graphql/",
            {
                "query": """query {
                            S_products(
                                first: %s
                                onlyUnmapped: false
                                sort: CREATED_AT_DESC
                                search: "%s"
                                ) {
                                edges {
                                node {
                                    id
                                    name
                                    languages
                                    regions { code }
                                    releasedAt
                                    createdAt
                                    slug
                                    type { value }
                                    auctions(first: 1) {
                                    edges {
                                        node {
                                        belongsToYou
                                        isInStock
                                        merchantName
                                        price { amount currency }
                                        }
                                    }
                                    }
                                }
                                }
                            }}"""
                % (count, product_name)
            },
        )
        data = dict(remove_edges_and_nodes(response.json()["data"]))

        return data["S_products"]


@timed_lru_cache(210000)
def get_access_token() -> str:
    response = requests.post(
        "{}/{}".format(settings.ENEBA_BASE_URI, "oauth/token"),
        data={
            "client_id": settings.ENEBA_CLIENT_ID,
            "grant_type": settings.ENEBA_GRANT_TYPE,
            "id": settings.ENEBA_ID,
            "secret": settings.ENEBA_SECRET,
        },
    ).json()

    return response.get("access_token")


def remove_edges_and_nodes(data) -> Dict | List:
    if isinstance(data, list):
        return [remove_edges_and_nodes(item) for item in data if item is not None]
    elif isinstance(data, dict):
        if "edges" in data:
            return remove_edges_and_nodes(data["edges"])
        elif "node" in data:
            return remove_edges_and_nodes(data["node"])
        else:
            return {key: remove_edges_and_nodes(value) for key, value in data.items()}
    else:
        return data
