from app.services import MESSAGES


def test_health(client):
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_match(client):
    response = client.get("/api/match/")

    assert response.status_code == 200
    data = response.json()
    assert data["matched"] is True
    assert data["message"] == ("Вы ищете DevOps. Я ищу команду. Мы идеально подходим друг-другу 💙")


def test_notification(client):
    response = client.get("/api/notification/")

    assert response.status_code == 200
    assert response.json()["message"] in MESSAGES
