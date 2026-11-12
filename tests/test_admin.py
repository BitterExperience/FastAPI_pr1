def test_list_users_as_admin(admin_client):
    response = admin_client.get("/admin/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(u["username"] == "testadmin" for u in data)


def test_list_users_as_user(auth_client):
    response = auth_client.get("/admin/users")
    assert response.status_code == 403


def test_block_user(admin_client):
    new_user = admin_client.post("/users/register",
                                 json={"username": "new_user",
                                       "email": "new@examplr.com",
                                       "password": "passwrod123"
                                       })
    assert new_user.status_code == 201
    new_user_id = new_user.json()["id"]
    response = admin_client.patch(f"/admin/users/{new_user_id}/block")
    assert response.status_code == 200
    assert response.json()["is_active"] == False


def test_delete_self(admin_client):
    response_data_me = admin_client.get("/users/me")
    assert response_data_me.status_code == 200
    me_id = response_data_me.json()["id"]
    me_del = admin_client.delete(f"/admin/users/{me_id}")
    assert me_del.status_code == 400
