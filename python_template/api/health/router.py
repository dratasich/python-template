"""
Health check endpoints.

Kubernetes uses these to determine if the service is healthy.
- liveness: is the service running? if not, restart it.
- readiness: is the service able to handle requests?

Because these are internal endpoints, we exclude them from the OpenAPI schema.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger

from python_template.infrastructure.db import DatabaseClient

from .status import Liveness, Readiness, SimpleStatus, Status

router = APIRouter(tags=["health"])


async def get_db(req: Request):
    return req.app.state.db


@router.get("/ready", response_model=Readiness, include_in_schema=False)
async def readiness_probe(
    db: Annotated[DatabaseClient, Depends(get_db)],
):
    """Checks connections to dependent services are healthy."""
    # default: all ready
    probe = Readiness(
        db=Status(status=SimpleStatus.up, details={}),
    )
    try:
        # check/ping the dependencies
        if not db.is_connected():
            probe.db = Status(status=SimpleStatus.down, details={})
    except Exception as e:
        logger.exception(e)
        probe.db = Status(status=SimpleStatus.down, details={"error": str(e)})
    if probe.is_down():
        return JSONResponse(status_code=503, content=probe.model_dump())
    return probe  # return 200 + readiness info


@router.get("/live", response_model=Liveness, include_in_schema=False)
async def liveness_probe():
    """Checks health of this service."""
    return Liveness(webserver=SimpleStatus.up)
