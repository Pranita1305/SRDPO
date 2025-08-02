def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["msg"]
