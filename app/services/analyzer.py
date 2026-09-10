from app.models.schemas import AnalysisResult, ModelMetadata, ScoreBreakdown
from app.services.llm_client import LLMClient
from app.services.rules import (
    COMPLEMENTARY,
    EDUCATION_MARKERS,
    SKILLS,
    present_terms,
    ratio_score,
    years_experience,
)


class AnalyzerService:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def analyze(self, cv_text: str, job_text: str) -> AnalysisResult:
        cv_skills = present_terms(cv_text, SKILLS)
        job_skills = present_terms(job_text, SKILLS)
        essential = job_skills - COMPLEMENTARY
        complementary = job_skills & COMPLEMENTARY
        strengths = sorted(cv_skills & job_skills)
        gaps = sorted(job_skills - cv_skills)

        cv_years, required_years = years_experience(cv_text), years_experience(job_text)
        cv_education = present_terms(cv_text, EDUCATION_MARKERS)
        job_education = present_terms(job_text, EDUCATION_MARKERS)
        breakdown = ScoreBreakdown(
            essential_skills=ratio_score(len(cv_skills & essential), len(essential), 60),
            experience=ratio_score(min(cv_years, required_years), required_years, 20),
            education=ratio_score(len(cv_education & job_education), len(job_education), 10),
            complementary_skills=ratio_score(len(cv_skills & complementary), len(complementary), 10),
        )
        score = round(sum(breakdown.model_dump().values()))
        llm_data = self.llm.extract(cv_text, job_text)
        recommendations = [f"Desarrollar y evidenciar experiencia práctica en {gap}." for gap in gaps[:3]]
        generic = [
            "Cuantificar los logros profesionales con resultados verificables.",
            "Adaptar el resumen profesional a los requisitos prioritarios del cargo.",
            "Agregar proyectos o certificaciones que demuestren las competencias faltantes.",
        ]
        recommendations.extend(generic[: max(0, 3 - len(recommendations))])
        level = "alta" if score >= 75 else "media" if score >= 50 else "baja"
        summary = llm_data.get("context_summary") or (
            f"Compatibilidad {level}: {len(strengths)} coincidencias y {len(gaps)} brechas identificadas."
        )
        warnings = list(llm_data.get("warnings", []))
        if not job_skills:
            warnings.append("El perfil no contiene competencias reconocibles; revise su nivel de detalle.")
        return AnalysisResult(
            compatibility_score=score,
            summary=summary,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            warnings=warnings,
            score_breakdown=breakdown,
            model_metadata=ModelMetadata(provider=self.llm.provider, model=self.llm.model, mode=self.llm.mode),
        )
