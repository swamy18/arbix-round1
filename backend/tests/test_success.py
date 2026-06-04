from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_score_happy_path() -> None:
    response = client.post(
        "/score",
        json={
            "land_area_acres": 5,
            "crop_type": "Rice",
            "repayment_history_score": 80,
            "annual_income_band": "5-10L",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert "request_id" in body
    assert body["score"] == 76
    assert body["reason_codes"] == [
        "good_repayment",
        "small_landholding",
        "mid_income_band",
    ]
    assert "timestamp" in body
