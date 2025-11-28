from uuid import UUID

from pytest import LogCaptureFixture
from starlette.testclient import TestClient


def test_missing_request_id(client: TestClient):
    resp = client.get("/ping")
    assert "X-Request-ID" in resp.headers
    rid = resp.headers["X-Request-ID"]
    assert isinstance(UUID(rid), UUID)


def test_bound_logger_has_request_id(client: TestClient, caplog: LogCaptureFixture):
    resp = client.get("/ping")
    rid = resp.headers["X-Request-ID"]
    # each log line should have the request_id in extra
    assert all(record.extra.get("request_id", "") == rid for record in caplog.records)  # type: ignore


def test_propagates_given_request_id(client: TestClient):
    header = "X-Request-ID"
    given = "whatever-id-you-want"
    resp = client.get("/ping", headers={header: given})
    assert resp.headers.get(header) == given
    resp = client.get("/ping", headers={header.lower(): given+"2"})
    assert resp.headers.get(header) == given+"2"
