import requests


class BaseClient:
    """Simple HTTP Client for http calls."""

    def __init__(self, base_url: str, token: str = "", timeout: int = 15):
        self.base_url = base_url
        self.token = token
        self.headers = self._get_headers()
        self.timeout = timeout

    def _get_headers(self):
        headers = {}
        headers["authorization"] = f"Bearer {self.token}"
        headers["content-type"] = "application/json"
        return headers

    def get(self, path, params=None):
        return requests.get(
            "{}/{}".format(self.base_url, path),
            params=params,
            headers=self.headers,
            timeout=self.timeout,
        )

    def post(self, path, data):
        return requests.post(
            "{}/{}".format(self.base_url, path),
            data=data,
            headers=self.headers,
            timeout=self.timeout,
        )

    def post_json(self, path, data):
        return requests.post(
            "{}/{}".format(self.base_url, path),
            json=data,
            headers=self.headers,
            timeout=self.timeout,
        )

    def delete(self, path, data=None, params=None):
        return requests.delete(
            "{}/{}".format(self.base_url, path),
            data=data,
            params=params,
            headers=self.headers,
            timeout=self.timeout,
        )
