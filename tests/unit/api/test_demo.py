from unittest.mock import patch

from python_template.config import Configuration


@patch.object(Configuration, "model_dump", return_value=Configuration().model_dump())
def test_default_config(mock_model_dump, client):
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    cfg = Configuration(**response.json())
    assert not cfg.log_json
    assert not cfg.my_list


def test_get_existing_item(client):
    response = client.get("/api/v1/item/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "item1"
    assert data["description"] == "A demo item retrieved from the repository."


def test_get_nonexistent_item(client):
    response = client.get("/api/v1/item/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"


def test_bad_request(client):
    bad_item = {
        "name": 123,  # should be a string
    }
    response = client.post("/api/v1/item", json=bad_item)
    assert response.status_code == 422


def test_create_item(client):
    new_item = {
        "name": "NewItem",
        "description": "This is a newly created item.",
    }
    response = client.post("/api/v1/item", json=new_item)
    assert response.status_code == 201
    item_id = response.json()
    assert item_id == 3

    # verify the item was persisted and can be retrieved
    get_response = client.get(f"/api/v1/item/{item_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["name"] == "NewItem"
