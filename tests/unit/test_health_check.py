from fastapi import status


def test_health_check(test_app):
    response = test_app.get("/api/v1/health-check")

    response.status_code = status.HTTP_200_OK
