import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.asyncio
async def test_healthcheck_handler(app: FastAPI, client: TestClient):
    url = app.url_path_for("healthcheck_handler")
    response: Response = client.get(url=url)

    assert response.is_success

    json_data = response.json()

    assert json_data["detail"] == "ok"
    assert json_data["result"] == "working"
