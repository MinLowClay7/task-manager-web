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

# Tests para asegurar que un token inválido no permite acceder a las tareas
def test_get_tasks_invalid_token(client):
    response = client.get(
        "/tasks/",
        headers={"Authorization": "Bearer token_invalido"}
    )

    assert response.status_code == 401

# Tests para asegurar que sin token no se pueden acceder a las tareas
def test_get_tasks_without_token(client):
    response = client.get("/tasks/")
    assert response.status_code == 401

# Tests para asegurar que no se puede actualizar una tarea que no existe
def test_update_nonexistent_task(client):
    token = create_user_and_token(
        client, "user@test.com", "password123"
    )

    response = client.put(
        "/tasks/9999",
        json={"title": "No existe"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

# Tests para asegurar que no se puede eliminar una tarea que no existe
def test_partial_update_task(client):
    token = create_user_and_token(
        client, "user2@test.com", "password123"
    )

    task = client.post(
        "/tasks/",
        json={"title": "Solo titulo"},
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    response = client.put(
        f"/tasks/{task['id']}",
        json={"completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["completed"] is True
    assert data["title"] == "Solo titulo"

# Tests para asegurar que eliminar una tarea dos veces da error la segunda vez
def test_delete_task_twice(client):
    token = create_user_and_token(
        client, "user3@test.com", "password123"
    )

    task = client.post(
        "/tasks/",
        json={"title": "Borrar"},
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    r1 = client.delete(
        f"/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    r2 = client.delete(
        f"/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert r1.status_code == 204
    assert r2.status_code == 204

# Tests para asegurar que un usuario no puede eliminar la tarea de otro
def test_user_cannot_delete_other_task(client):
    token1 = create_user_and_token(
        client, "a@test.com", "password123"
    )
    token2 = create_user_and_token(
        client, "b@test.com", "password123"
    )

    task = client.post(
        "/tasks/",
        json={"title": "Privada"},
        headers={"Authorization": f"Bearer {token1}"}
    ).json()

    response = client.delete(
        f"/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 204
