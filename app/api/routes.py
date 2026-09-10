import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.config import Settings, get_settings
from app.models.schemas import AnalysisResult, AnalyzeRequest, ExampleCase, HealthResponse
from app.services.analyzer import AnalyzerService
from app.services.llm_client import LLMError, LLMTimeoutError

router = APIRouter()


def analyzer_from_request(request: Request) -> AnalyzerService:
    return request.app.state.analyzer


@router.get("/health", response_model=HealthResponse, tags=["operación"])
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(version=settings.app_version, model_ready=settings.model_ready)


@router.post("/api/v1/analyze", response_model=AnalysisResult, tags=["análisis"])
def analyze(payload: AnalyzeRequest, service: AnalyzerService = Depends(analyzer_from_request)) -> AnalysisResult:
    try:
        return service.analyze(payload.cv_text, payload.job_profile_text)
    except LLMTimeoutError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/api/v1/examples", response_model=list[ExampleCase], tags=["ejemplos"])
def examples() -> list[ExampleCase]:
    path = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "examples.json"
    return [ExampleCase.model_validate(item) for item in json.loads(path.read_text(encoding="utf-8"))]
