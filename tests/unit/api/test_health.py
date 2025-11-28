from unittest.mock import patch

from python_template.api.health.status import SimpleStatus
from python_template.infrastructure.db import DatabaseClient


def test_liveness_returns_200(client):
    response = client.get("/live")
    assert response.status_code == 200


def test_readiness_returns_200_when_db_connected(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["db"]["status"] == SimpleStatus.up.value


@patch.object(DatabaseClient, "is_connected", return_value=False)
def test_readiness_returns_503_when_db_disconnected(mock_disconnected, client):
    client.app.state.db.is_connected = mock_disconnected
    response = client.get("/ready")
    assert response.status_code == 503
    data = response.json()
    assert data["db"]["status"] == SimpleStatus.down.value
