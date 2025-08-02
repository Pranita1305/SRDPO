from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_dashboard_endpoint():
    response = client.get("/dashboard/data")
    assert response.status_code in [200, 401]  # Unauthorized if no token
