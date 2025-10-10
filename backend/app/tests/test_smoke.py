"""Smoke tests to verify test infrastructure is working correctly."""
import pytest


def test_app_imports() -> None:
    """Verify that the FastAPI app can be imported without errors."""
    from app.main import app
    
    assert app is not None
    assert app.title == "TSV-RSM Backend"


@pytest.mark.asyncio
async def test_client_fixture_works(client) -> None:
    """Verify that the async test client fixture is configured correctly."""
    assert client is not None
    
    response = await client.get("/health")
    assert response.status_code == 200
