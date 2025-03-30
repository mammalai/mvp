import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app import create_app

@pytest_asyncio.fixture(loop_scope="session")
async def client():
    """
    Fixture to provide an AsyncClient for testing FastAPI endpoints.
    """
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(loop_scope="session")
def strong_password():
    return "StrongPassword123"

@pytest_asyncio.fixture(autouse=True, loop_scope="session")
async def test_database():
    """Use a separate test database and clean it before each test function."""
    # Store original db name
    original_db_name = os.environ.get("MONGO_DB_NAME")
    
    # Use a test-specific database
    test_db_name = f"{original_db_name}"
    os.environ["MONGO_DB_NAME"] = test_db_name
    
    # Create new connection using the current running loop
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    test_client = AsyncIOMotorClient(mongo_uri)
    test_db = test_client[test_db_name]
    
    # Clear all collections
    collections = await test_db.list_collection_names()
    for collection in collections:
        await test_db[collection].delete_many({})
    
    # Replace the global db with test db (monkey patch)
    import backend.extensions
    backend.extensions.db = test_db
    
    yield
    
    # Optionally drop the test database
    await test_client.drop_database(test_db_name)
    
    # Restore original setting
    os.environ["MONGO_DB_NAME"] = original_db_name
