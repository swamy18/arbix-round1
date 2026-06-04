from dataclasses import dataclass

try:
    from .models import AnnualIncomeBand, ScoreRequest
except ImportError:
    from models import AnnualIncomeBand, ScoreRequest


@dataclass(frozen=True)
class ScoreResult:
    score: int
    reason_codes: list[str]


def _repayment_reason(repayment_history_score: int) -> tuple[int, str]:
    if repayment_history_score >= 75:
        return repayment_history_score, "good_repayment"
    if repayment_history_score >= 50:
        return repayment_history_score, "average_repayment"
    return repayment_history_score, "poor_repayment"


def _land_contribution(land_area_acres: float) -> tuple[int, str]:
    if land_area_acres > 10:
        return 20, "high_landholding"
    if land_area_acres > 5:
        return 12, "medium_landholding"
    return 5, "small_landholding"


def _income_contribution(annual_income_band: AnnualIncomeBand) -> tuple[int, str]:
    if annual_income_band == AnnualIncomeBand.BELOW_2L:
        return 5, "low_income_band"
    if annual_income_band == AnnualIncomeBand.BETWEEN_2_5L:
        return 10, "lower_mid_income_band"
    if annual_income_band == AnnualIncomeBand.BETWEEN_5_10L:
        return 15, "mid_income_band"
    return 20, "high_income_band"


def calculate_score(payload: ScoreRequest) -> ScoreResult:
    repayment_points, repayment_reason = _repayment_reason(
        payload.repayment_history_score
    )
    land_points, land_reason = _land_contribution(payload.land_area_acres)
    income_points, income_reason = _income_contribution(payload.annual_income_band)

    raw_score = round((repayment_points * 0.7) + land_points + income_points)
    final_score = max(0, min(100, raw_score))

    return ScoreResult(
        score=final_score,
        reason_codes=[repayment_reason, land_reason, income_reason],
    )
