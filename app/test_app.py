import json
from app import app

import pytest


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_generate_phrase(client):
    input_data = {"input_string": "elephant"}
    response = client.post("/generate_phrase", json=input_data)

    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert "phrase" in data
    assert "is_palindrome" in data
