def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "description": "Testing is important"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data

# Tests para listar tareas
def test_get_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Tests para actualizar una tarea
def test_update_task(client):
    task = client.post("/tasks/", json={"title": "Update me"}).json()

    response = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Updated", "completed": True}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Updated"
    assert data["completed"] is True

# Tests para eliminar una tarea
def test_delete_task(client):
    task = client.post("/tasks/", json={"title": "Delete me"}).json()

    response = client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 204

