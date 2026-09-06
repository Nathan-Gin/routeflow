from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/health")

    """
    assert means i expect that the condition is true,
    if it isn't fail the test
    """
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_calculate_route():
    app = create_app()
    client = app.test_client()
    
    response = client.post(
        "/api/routes/calculate",
        json={
            "start": "A",
            "destination": "F",
            "algorithm": "dijkstra"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "path" in data
    assert "distance" in data
    assert "nodes_explored" in data

    assert data["path"][0] == "A"
    assert data["path"][-1] == "F"