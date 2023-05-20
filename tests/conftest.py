import asyncio

import pytest
from starlette.testclient import TestClient

from src.config import Settings, get_settings
from src.database import drop_test_database
from src.main import create_application
from src.plugins.eneba import EnebaClient
from src.plugins.ezpin import Ezpin

from .mocks.eneba import EnebaClient as MockEnebaClient
from .mocks.ezpin import Ezpin as MockEzpin


def get_settings_override() -> Settings:
    return Settings(
        DATABASE_NAME="test",
        ENVIRONMENT="test",
        ENEBA_CALL_LIMIT=1,
        ENEBA_CALL_LIMIT_PERIOD=1,
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
    app.dependency_overrides[EnebaClient] = MockEnebaClient
    app.dependency_overrides[Ezpin] = MockEzpin

    with TestClient(app) as test_client:
        yield test_client
    asyncio.run(drop_test_database())
