
def test_register_success(client):
    response = client.post("/users/register",
                           json={
                               "username": "new_user",
                               "email": "new_email@example.com",
                               "password": "secret123"
                           })
    assert response.status_code == 201
    assert response.json()["username"] == "new_user"
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()


def test_register_duplicate_username(client, test_user):
    response = client.post("/users/register",
                           json={
                               "username": "testuser",
                               "email": "user@example.com",
                               "password": "secret123"
                           })
    assert response.status_code == 409


def test_login_success(client, test_user):
    response = client.post("/users/login",
                           data={
                               "username": test_user["username"],
                               "password": test_user["password"]
                           })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post("/users/login",
                           data={
                               "username": test_user["username"],
                               "password": "incorrect"
                           })
    assert response.status_code == 401
