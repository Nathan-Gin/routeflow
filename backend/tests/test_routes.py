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