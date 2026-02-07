def create_user_and_token(client, email, password):
    client.post(
        "/users/",
        json={"email": email, "password": password},
    )

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    return response.json()["access_token"]

def test_create_task_authenticated(client):
    token = create_user_and_token(
        client,
        "user1@test.com",
        "password123"
    )

    response = client.post(
        "/tasks/",
        json={"title": "Task protegida"},
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Task protegida"

def test_create_task_unauthorized(client):
    response = client.post(
        "/tasks/",
        json={"title": "No debería crear"},
    )

    assert response.status_code == 401

# Tests para listar tareas
def test_get_tasks(client):
    token = create_user_and_token(
        client, "test@test.com", "password123"
    )

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Tests para actualizar una tarea
def test_update_task(client):
    token = create_user_and_token(
        client, "user@test.com", "password123"
    )

    task = client.post(
        "/tasks/",
        json={"title": "Update me"},
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    response = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Updated", "completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["completed"] == True

# Tests para eliminar una tarea
def test_delete_task(client):
    token = create_user_and_token(
        client, "user@test.com", "password123"
    )

    task = client.post(
        "/tasks/",
        json={"title": "Update me"},
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    response = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Updated", "completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["completed"] == True

# Tests para asegurar que un usuario no puede ver las tareas de otro
def test_user_cannot_see_other_tasks(client):
    token1 = create_user_and_token(
        client, "u1@test.com", "pass1234"
    )
    token2 = create_user_and_token(
        client, "u2@test.com", "pass1234"
    )

    client.post(
        "/tasks/",
        json={"title": "Task privada"},
        headers={"Authorization": f"Bearer {token1}"},
    )

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 200
    assert response.json() == []
