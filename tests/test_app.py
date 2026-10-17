import pytest
from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "test.db"),
    })
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_student_and_marks_workflow(client):
    response = client.post("/api/students", json={
        "name": "Asha Patil",
        "email": "asha@example.com",
        "course": "Computer Science",
    })
    assert response.status_code == 201
    student_id = response.json["id"]

    response = client.post("/api/marks", json={
        "student_id": student_id,
        "subject": "Cloud Computing",
        "score": 92,
    })
    assert response.status_code == 201
    assert response.json["score"] == 92

    assert len(client.get("/api/students").json) == 1
    assert len(client.get("/api/marks").json) == 1


def test_student_validation(client):
    response = client.post("/api/students", json={"name": "Incomplete"})
    assert response.status_code == 400


def test_duplicate_email(client):
    student = {
        "name": "Asha Patil",
        "email": "asha@example.com",
        "course": "Computer Science",
    }
    assert client.post("/api/students", json=student).status_code == 201
    assert client.post("/api/students", json=student).status_code == 409


def test_marks_reject_invalid_score(client):
    student = client.post("/api/students", json={
        "name": "Asha Patil",
        "email": "asha@example.com",
        "course": "Computer Science",
    }).json

    response = client.post("/api/marks", json={
        "student_id": student["id"],
        "subject": "Cloud Computing",
        "score": 120,
    })
    assert response.status_code == 400
