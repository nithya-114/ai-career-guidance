import sys
import os
import json
import pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_login_success(client):
    response = client.post(
        "/login",
        data=json.dumps({
            "email": "anu@student.com",
            "password": "student123"
        }),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert "token" in response.json


def test_login_wrong_password(client):
    response = client.post(
        "/login",
        data=json.dumps({
            "email": "anu@student.com",
            "password": "wrongpassword"
        }),
        content_type="application/json"
    )

    assert response.status_code == 401


def test_login_user_not_found(client):
    response = client.post(
        "/login",
        data=json.dumps({
            "email": "unknown@gmail.com",
            "password": "123456"
        }),
        content_type="application/json"
    )

    assert response.status_code == 404
