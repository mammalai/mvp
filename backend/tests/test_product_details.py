import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import pytest_asyncio
from httpx import AsyncClient

@pytest.mark.asyncio(loop_scope="session")
async def test_insert_product_details(client: AsyncClient):
    # Payload based on the provided JSON; required fields added for model compliance.
    data = {
        "title": "Raised Toilet Seat",
        "category": "Bathroom",             # added required field
        "price_estimate": "$80",            # added required field
        "usefulness_knee_hip_surgery": "medium",  # added required field
        "usefulness_stroke_and_brain_injury": "medium",  # added required field
        "usefulness_aging_in_place": "medium", # added required field
        "initial_description": "Raising your toilet height by 3-5 inches makes sitting and standing easier. While set-on seats are good travel options, occupational therapists recommend clamp-on or bolt-on options for better safety and stability.",
        "product_table": [
            {
                "category": "top_pick",
                "why_this_one": [
                    "This clamp-on riser adds 5 inches and provides exceptional stability and comfort.",
                    "Available in round and elongated versions with a subtle design."
                ],
                "price": "$86.99",
                "link": "https://www.amazon.com/Bemis-7YE85310TSS-Larger-Shield..."
            },
            {
                "category": "budget_pick",
                "why_this_one": [
                    "This bolt-on riser adds 3.5 inches and is a great budget option.",
                    "Available in round and elongated versions."
                ],
                "price": "$29.99",
                "link": "https://www.amazon.com/Drive-Medical-12067-Raised-Toilet..."
            }
        ],
        "what_to_look_for": {
            "description": "A good riser should be sturdy, easy to clean, and fit well. Check the height and toilet shape, and consider handles for extra support.",
            "no_brainers": [
                "Height: Choose a height that makes sitting and standing easier.",
                "Stability: Look for a seat that is stable and secure.",
                "Shape: Choose a round or elongated seat based on your toilet shape."
            ],
            "things_to_think_about": [
                "Installation: Consider how easy it is to install the seat.",
                "Cleaning: Look for a seat that is easy to clean."
            ]
        },
        "more_to_consider": "<b>Finding Your Perfect Height</b>: Before buying, measure from the back of your knees to the floor while seated, then subtract your current toilet height. This gives you your ideal riser height. Your knees should be slightly higher than your hips when seated.\nInstallation Options:\nLong-Term Use: We recommend bolt-on risers for maximum stability. The Bemis Assurance (3-inch height) comes with or without handles. Consider the handle-free version paired with a wall-mounted grab bar for a cleaner look. For a budget-friendly option with handles, try the Vive Health riser (3.5-inch height).\nTemporary Use: Clamp-on risers offer easy installation and removal. For round toilets, we recommend the Vaunn (4.5-inch height). For elongated toilets, try the Carex (5-inch height).\n\nWith the right toilet riser installed correctly, you'll enjoy safer, more confident bathroom visits. A stable, well-fitted riser reduces strain on joints and muscles while supporting recovery and independence."
    }
    response = await client.post("/api/product-details/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == data["title"]

@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_details(client: AsyncClient):
    # Insert a product_details record to update
    data_create = {
        "title": "Initial Raised Toilet Seat",
        "category": "Bathroom",
        "price_estimate": "$75",
        "usefulness_knee_hip_surgery": "low",
        "usefulness_stroke_and_brain_injury": "low",
        "usefulness_aging_in_place": "low",
        "initial_description": "Initial description",
        "product_table": [],
        "what_to_look_for": {
            "description": "Initial guidelines",
            "no_brainers": [],
            "things_to_think_about": []
        },
        "more_to_consider": "Initial considerations"
    }
    response_create = await client.post("/api/product-details/", json=data_create)
    assert response_create.status_code == 200
    product_details = response_create.json()
    product_details_id = product_details["id"]

    # Update the product_details record
    data_update = data_create.copy()
    data_update["title"] = "Updated Raised Toilet Seat"
    response_update = await client.post(f"/api/product-details/{product_details_id}", json=data_update)
    assert response_update.status_code == 200
    updated_details = response_update.json()
    assert updated_details["title"] == "Updated Raised Toilet Seat"

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_details(client: AsyncClient):
    # Insert a product_details record to delete
    data_create = {
        "title": "Delete Test Raised Toilet Seat",
        "category": "Bathroom",
        "price_estimate": "$60",
        "usefulness_knee_hip_surgery": "high",
        "usefulness_stroke_and_brain_injury": "high",
        "usefulness_aging_in_place": "high",
        "initial_description": "Delete test description",
        "product_table": [],
        "what_to_look_for": {
            "description": "Delete test guidelines",
            "no_brainers": [],
            "things_to_think_about": []
        },
        "more_to_consider": "Delete considerations"
    }
    response_create = await client.post("/api/product-details/", json=data_create)
    assert response_create.status_code == 200
    product_details = response_create.json()
    product_details_id = product_details["id"]
    
    response_delete = await client.delete(f"/api/product-details/{product_details_id}")
    assert response_delete.status_code == 200
    result = response_delete.json()
    assert "deleted" in result.get("message", "").lower()
