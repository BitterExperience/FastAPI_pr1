
def test_process_time_header(client):
    response = client.get("/api/v1/books")
    assert "x-process-time" in response.headers
    assert float(response.headers["x-process-time"]) >= 0

