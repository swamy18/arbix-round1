from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_score_validation_error() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 0,
            "crop_type": "   ",
            "repayment_history_score": 120,
            "annual_income_band": "invalid-band",
        },
    )

    assert response.status_code == 422
    body = response.json()

    assert "request_id" in body
    assert "timestamp" in body
    assert len(body["detail"]) >= 3
