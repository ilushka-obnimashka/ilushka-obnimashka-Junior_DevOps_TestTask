from app.services import MESSAGES


def test_health_reports_live_backend(client):
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"].startswith("application/json")
    assert response.headers["cache-control"] == "no-store"


def test_match_contract_and_method(client):
    response = client.get("/api/match/")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {"matched", "message"}
    assert payload["matched"] is True
    assert isinstance(payload["message"], str)
    assert payload["message"].strip()
    assert response.headers["cache-control"] == "no-store"
    assert client.post("/api/match/").status_code == 405


def test_notification_uses_service_result(client, monkeypatch):
    # Control the random choice without replacing the route or its service.
    marker = "Уникальная фраза тестового backend"
    received_sequences = []

    def controlled_choice(sequence):
        received_sequences.append(sequence)
        return marker

    monkeypatch.setattr("app.services.secrets.choice", controlled_choice)
    response = client.get("/api/notification/")

    assert response.status_code == 200
    assert received_sequences == [MESSAGES]
    assert response.json() == {"message": marker}
    assert response.headers["cache-control"] == "no-store"
