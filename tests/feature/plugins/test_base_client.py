from fastapi import status

from src.plugins.base_client import BaseClient

client = BaseClient("https://google.com", "random-token")


def test_get():
    response = client.get(path="")
    assert response.status_code == status.HTTP_200_OK


def test_post():
    response = client.post(path="", data={})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_post_json():
    response = client.post_json(path="", data={})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_delete():
    response = client.delete(path="")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
