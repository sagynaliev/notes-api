from app.app import app


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_healthz():
    client = app.test_client()
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_create_and_get_note():
    client = app.test_client()

    response = client.post(
        "/notes",
        json={"text": "Learn DevOps"}
    )

    assert response.status_code == 201

    response = client.get("/notes")

    assert response.status_code == 200
    assert len(response.get_json()) >= 1


def test_get_notes_empty():
    client = app.test_client()

    response = client.get("/notes")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_note_without_text():
    client = app.test_client()

    response = client.post(
        "/notes",
        json={}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "text is required"
