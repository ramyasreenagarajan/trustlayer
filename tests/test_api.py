import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

pytestmark = pytest.mark.skipif(
    not (ROOT / "models" / "deploy" / "model.joblib").exists(),
    reason="model not built yet (run: py src/build_deploy_model.py)",
)

from fastapi.testclient import TestClient  # noqa: E402
from api.main import app, limiter  # noqa: E402

client = TestClient(app)
SCAM = "Dear customer, your SBI account will be blocked today. Update KYC immediately: bit.ly/sbi-kyc-upd"


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_analyze_returns_expected_fields():
    r = client.post("/analyze", json={"message": SCAM})
    assert r.status_code == 200
    body = r.json()
    for key in ["verdict", "score", "label", "probabilities", "signs", "influential_words", "advice", "disclaimer"]:
        assert key in body
    assert 0 <= body["score"] <= 100


def test_scam_is_not_low_risk():
    assert client.post("/analyze", json={"message": SCAM}).json()["verdict"] != "Low risk"


def test_too_short_too_long_and_missing_are_rejected():
    assert client.post("/analyze", json={"message": "ab"}).status_code == 422
    assert client.post("/analyze", json={"message": "x" * 2001}).status_code == 422
    assert client.post("/analyze", json={}).status_code == 422


def test_bad_language_is_rejected():
    assert client.post("/analyze", json={"message": SCAM, "lang": "xx"}).status_code == 422


def test_huge_body_is_rejected():
    assert client.post("/analyze", json={"message": "x" * 20000}).status_code == 413


def test_cors_allows_local_site():
    r = client.post("/analyze", json={"message": SCAM}, headers={"Origin": "http://localhost:5500"})
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5500"


def test_rate_limit_eventually_returns_429():
    limiter.reset()
    codes = [client.post("/analyze", json={"message": SCAM}).status_code for _ in range(40)]
    limiter.reset()
    assert 429 in codes