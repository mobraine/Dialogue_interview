from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_inference():
    response = client.get("/v1/inference?days_to_forecast=30")
    assert response.status_code == 200
    assert "forecast" in response.json()

def test_update_data():
    response = client.post(
        "/v1/update-data",
        files={"file": ("test.csv", "column1,column2\nvalue1,value2", "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Data updated successfully"}