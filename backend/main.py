import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import CORS_ORIGINS
from backend.database import init_db
from backend.routes.datasets import router as datasets_router
from backend.routes.evaluations import router as evaluations_router
from backend.routes.health import router as health_router
from backend.routes.models import router as models_router
from backend.routes.robustness import router as robustness_router
from backend.utils.exceptions import AppException
from backend.utils.logger import get_logger, setup_logging
from backend.utils.response import error_response, success_response

setup_logging()
logger = get_logger(__name__)

app = FastAPI(title="AI Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    logger.info("Database initialized")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info("%s %s %.2fms", request.method, request.url.path, duration_ms)
    return response


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response("Request failed", exc.message),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response("Request failed", str(exc.detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_response("Validation failed", "Invalid request payload", {"details": exc.errors()}),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content=error_response("Internal server error", "Unexpected error occurred"),
    )


@app.get("/")
def root():
    return success_response({"service": "ai-platform-backend"}, "API is running")


app.include_router(health_router)
app.include_router(models_router)
app.include_router(datasets_router)
app.include_router(evaluations_router)
app.include_router(robustness_router)
