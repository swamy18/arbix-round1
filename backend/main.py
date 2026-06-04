from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

try:
    from .logger import get_logger
    from .models import ScoreRequest, ScoreResponse
    from .scoring import calculate_score
except ImportError:
    from logger import get_logger
    from models import ScoreRequest, ScoreResponse
    from scoring import calculate_score

app = FastAPI(title="Scoring Service", version="1.0.0")
logger = get_logger()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    request_id = str(uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    logger.warning(
        "validation_failed path=%s errors=%s",
        request.url.path,
        exc.errors(),
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "request_id": request_id,
                "timestamp": timestamp,
                "detail": exc.errors(),
            }
        ),
    )


@app.post("/score", response_model=ScoreResponse, status_code=200)
async def score(payload: ScoreRequest) -> ScoreResponse:
    request_id = uuid4()
    timestamp = datetime.now(timezone.utc)
    result = calculate_score(payload)

    logger.info(
        (
            "score_calculated timestamp=%s land_area_acres=%s crop_type=%s "
            "repayment_history_score=%s annual_income_band=%s final_score=%s "
            "reason_codes=%s"
        ),
        timestamp.isoformat(),
        payload.land_area_acres,
        payload.crop_type,
        payload.repayment_history_score,
        payload.annual_income_band.value,
        result.score,
        result.reason_codes,
        extra={"request_id": str(request_id)},
    )

    return ScoreResponse(
        request_id=request_id,
        score=result.score,
        reason_codes=result.reason_codes,
        timestamp=timestamp,
    )
