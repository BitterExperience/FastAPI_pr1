
def test_cors_preflight(client):
    response = client.options("/api/v1/books",
                           headers={"Origin": "http://localhost:3000",
                                    "Access-Control-Request-Method": "GET"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_wrong_origin(client):
    response = client.options("/api/v1/books",
                              headers={"Origin": "http://evil.com",
                                       "Access-Control-Request-Method": "GET"})
    assert response.status_code == 400
    assert response.headers.get("access-control-allow-origin") != "http://evil.com"