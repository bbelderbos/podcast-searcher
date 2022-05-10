import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


def test_search(client):
    response = client.get("/?feed=https://feeds.buzzsprout.com/1501156.rss&term=ryan")
    assert response.status_code == 200
    assert len(response.json()) == 3
    # inspect the content
