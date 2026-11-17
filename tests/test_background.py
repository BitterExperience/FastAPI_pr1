from unittest.mock import patch


def test_register_mock(client):
    with patch("app.routers.user.send_welcome_email") as mock_send:
        response = client.post("/users/register",
                           json={
                               "username": "testuser2",
                               "email": "user_test2@example.com",
                               "password": "secret123",
                           })
        assert response.status_code == 201
        mock_send.assert_called_once()
        args, kwargs = mock_send.call_args
        assert args[0] == "user_test2@example.com"
        assert args[1] == "testuser2"
