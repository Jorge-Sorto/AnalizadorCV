import re
import unicodedata

SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c#",
    "asp.net",
    "fastapi",
    "react",
    "angular",
    "sql",
    "postgresql",
    "mysql",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git",
    "github actions",
    "ci/cd",
    "linux",
    "power bi",
    "excel",
    "scrum",
    "agile",
    "rest",
    "api",
    "machine learning",
    "ia",
    "comunicacion",
    "liderazgo",
    "ingles",
}
COMPLEMENTARY = {"git", "github actions", "ci/cd", "linux", "scrum", "agile", "ingles", "comunicacion", "liderazgo"}
EDUCATION_MARKERS = {"licenciatura", "ingenieria", "maestria", "tecnico", "universidad", "graduado", "egresado"}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def present_terms(text: str, vocabulary: set[str]) -> set[str]:
    normalized = normalize(text)
    return {term for term in vocabulary if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", normalized)}


def years_experience(text: str) -> int:
    values = [int(value) for value in re.findall(r"(\d{1,2})\s*(?:anos|año|años)", normalize(text))]
    return max(values, default=0)


def ratio_score(matches: int, required: int, weight: int) -> float:
    if required == 0:
        return float(weight)
    return round(min(matches / required, 1) * weight, 2)
