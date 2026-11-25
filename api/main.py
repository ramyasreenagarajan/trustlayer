import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from predict import analyze, _load  # noqa: E402

MAX_CHARS = 2000
MAX_BODY_BYTES = 10_000
RATE_LIMIT = os.environ.get("RATE_LIMIT", "20/minute")
ORIGINS = [o.strip() for o in os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500").split(",") if o.strip()]

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app):
    _load()  # load the model once at startup
    yield


app = FastAPI(title="TrustLayer API", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def limit_body(request: Request, call_next):
    length = request.headers.get("content-length")
    if length and length.isdigit() and int(length) > MAX_BODY_BYTES:
        return JSONResponse({"detail": "Request too large."}, status_code=413)
    return await call_next(request)


app.add_middleware(CORSMiddleware, allow_origins=ORIGINS,
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


class AnalyzeRequest(BaseModel):
    message: str = Field(min_length=3, max_length=MAX_CHARS)
    lang: str = Field(default="en", pattern="^(en|hi|ta)$")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
@limiter.limit(RATE_LIMIT)
def analyze_endpoint(request: Request, body: AnalyzeRequest):
    return analyze(body.message, body.lang)