import pytest
from starlette.testclient import TestClient

from src.config import Settings, get_settings
from src.main import create_application


def get_settings_override() -> Settings:
    return Settings(
        database_name="test",
        environment="test",
    )


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
        pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
        pytest.param(
            ("trio", {"restrict_keyboard_interrupt_to_checkpoints": True}), id="trio"
        ),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="session")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:
        yield test_client
