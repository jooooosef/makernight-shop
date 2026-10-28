from rest_framework.test import APIClient


def test_anyone_gets_the_status(api: APIClient) -> None:
    response = api.get("/api/v1/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
