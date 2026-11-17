
def test_process_time_header(client):
    response = client.get("/books")
    assert "x-process-time" in response.headers
    assert float(response.headers["x-process-time"]) >= 0

