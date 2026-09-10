import json
from abc import ABC, abstractmethod

from openai import APITimeoutError, OpenAI


class LLMError(RuntimeError):
    pass


class LLMTimeoutError(LLMError):
    pass


class LLMClient(ABC):
    provider: str
    model: str
    mode: str

    @abstractmethod
    def extract(self, cv_text: str, job_text: str) -> dict:
        """Extract evidence only; the deterministic service calculates the score."""


class DemoLLMClient(LLMClient):
    provider = "local"
    model = "deterministic-rules-v1"
    mode = "demo"

    def extract(self, cv_text: str, job_text: str) -> dict:
        return {"warnings": ["Análisis ejecutado en modo demostración sin proveedor externo."]}


class OpenAILLMClient(LLMClient):
    provider = "openai"
    mode = "live"

    def __init__(self, api_key: str, model: str, timeout: float) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key, timeout=timeout, max_retries=1)

    def extract(self, cv_text: str, job_text: str) -> dict:
        prompt = f"""Analiza los textos sin inventar antecedentes. Devuelve SOLO JSON con
las claves warnings (lista de advertencias sustentadas) y context_summary (resumen breve).
No calcules el puntaje. CV:\n{cv_text}\n\nPERFIL:\n{job_text}"""
        try:
            response = self.client.responses.create(model=self.model, input=prompt)
            data = json.loads(response.output_text)
        except APITimeoutError as exc:
            raise LLMTimeoutError("El proveedor excedió el tiempo de espera.") from exc
        except json.JSONDecodeError as exc:
            raise LLMError("El proveedor devolvió una respuesta fuera del contrato JSON.") from exc
        except Exception as exc:
            raise LLMError("No fue posible consultar el proveedor de IA.") from exc
        if not isinstance(data.get("warnings", []), list):
            raise LLMError("La respuesta del proveedor no cumple el contrato.")
        return data
