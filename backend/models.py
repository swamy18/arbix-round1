from datetime import datetime, timezone
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class AnnualIncomeBand(str, Enum):
    BELOW_2L = "<2L"
    BETWEEN_2_5L = "2-5L"
    BETWEEN_5_10L = "5-10L"
    ABOVE_10L = ">10L"


class ScoreRequest(BaseModel):
    land_area_acres: float = Field(..., gt=0)
    crop_type: str
    repayment_history_score: int = Field(..., ge=0, le=100)
    annual_income_band: AnnualIncomeBand

    @field_validator("crop_type")
    @classmethod
    def validate_crop_type(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("crop_type must be non-empty")
        return normalized


class ScoreResponse(BaseModel):
    request_id: UUID
    score: int = Field(..., ge=0, le=100)
    reason_codes: list[str] = Field(..., min_length=3, max_length=3)
    timestamp: datetime

    @field_validator("timestamp")
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
