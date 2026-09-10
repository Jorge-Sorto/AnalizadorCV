from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    cv_text: str = Field(min_length=100, max_length=30_000)
    job_profile_text: str = Field(min_length=100, max_length=30_000)

    @field_validator("cv_text", "job_profile_text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 100:
            raise ValueError("El texto debe contener al menos 100 caracteres útiles.")
        return value


class ScoreBreakdown(BaseModel):
    essential_skills: float = Field(ge=0, le=60)
    experience: float = Field(ge=0, le=20)
    education: float = Field(ge=0, le=10)
    complementary_skills: float = Field(ge=0, le=10)


class ModelMetadata(BaseModel):
    provider: str
    model: str
    mode: Literal["demo", "live"]


class AnalysisResult(BaseModel):
    compatibility_score: int = Field(ge=0, le=100)
    summary: str
    strengths: list[str]
    gaps: list[str]
    recommendations: list[str] = Field(min_length=3)
    warnings: list[str]
    score_breakdown: ScoreBreakdown
    model_metadata: ModelMetadata


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    version: str
    model_ready: bool


class ExampleCase(BaseModel):
    id: str
    level: Literal["alta", "media", "baja"]
    cv_text: str
    job_profile_text: str
