import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import pytest_asyncio
from httpx import AsyncClient
from backend.models import Product  # Assuming you have a Product model

# The following import ensures your client fixture is accessible
# This assumes you have a conftest.py with the client fixture
# If your fixture is elsewhere, adjust this import accordingly

@pytest.mark.asyncio(loop_scope="session")
async def test_insert_product(client):
    # Test inserting a new product
    data = {
        "name": "Test Product",
        "price_estimate": 99,
        "category": "Category A",
        "description": "A test product"
    }
    response = await client.post("/api/products/", json=data)
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == data["name"]
    # ...additional assertions as needed...

@pytest.mark.asyncio(loop_scope="session")
async def test_update_product(client):
    # First, insert a product to then update
    data_create = {
        "name": "Initial Product",
        "price_estimate": 200,
        "category": "Category B",
        "description": "Initial product"
    }
    response_create = await client.post("/api/products/", json=data_create)
    assert response_create.status_code == 200
    product = response_create.json()
    product_id = product["id"]

    # Update the product
    data_update = {
        "name": "Updated Product",
        "price_estimate": 250,
        "category": "Category B",
        "description": "Updated description"
    }
    response_update = await client.post(f"/api/products/{product_id}", json=data_update)
    assert response_update.status_code == 200
    updated_product = response_update.json()
    assert updated_product["name"] == "Updated Product"
    # ...additional assertions as needed...

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product(client):
    # Create a product to delete
    data_create = {
        "name": "Delete Test",
        "price_estimate": 50,
        "category": "Category C",
        "description": "To be deleted"
    }
    response_create = await client.post("/api/products/", json=data_create)
    assert response_create.status_code == 200
    product = response_create.json()
    product_id = product["id"]

    # Delete the product
    response_delete = await client.delete(f"/api/products/{product_id}")
    assert response_delete.status_code == 200
    result = response_delete.json()
    assert "deleted" in result.get("message", "").lower()
    # ...additional assertions as needed...
