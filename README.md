# Analizador inteligente de CV y perfil de cargo

Aplicación FastAPI que compara evidencia explícita de un CV con un perfil, calcula compatibilidad trazable y presenta fortalezas, brechas y recomendaciones.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Abrir `http://localhost:8000`; Swagger está en `/docs`.

## Configuración IA

El modo inicial `LLM_PROVIDER=demo` funciona sin credenciales. Para la integración real:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=su_clave_solo_en_el_entorno
OPENAI_MODEL=gpt-5-mini
```

Nunca versionar `.env`. El cliente usa la Responses API y rechaza timeout o JSON inválido con 503/502.

## Fórmula

`puntaje = esenciales (60) + experiencia (20) + formación (10) + complementarias (10)`.
Cada subtotal es `min(coincidencias/requisitos, 1) × peso`. Si una categoría no contiene requisitos, aporta su peso completo para no penalizar información que el perfil no exige. El LLM no calcula el puntaje.

## Calidad

```bash
ruff check app tests
pytest -q --cov=app --cov-report=term-missing --cov-fail-under=70
```

## Docker

```bash
cp .env.example .env
docker compose up -d --build
curl http://localhost:8000/health
```

## Despliegue

Preparar un VPS Ubuntu, clonar en `/opt/cv-job-analyzer`, crear `.env` únicamente en el servidor y ejecutar `docker compose up -d --build`. Configurar `SERVER_HOST`, `SERVER_USER` y `SERVER_SSH_KEY` en GitHub Secrets. El workflow despliega únicamente después de CI verde.

## Entrega académica pendiente

Crear un repositorio GitHub, trabajar en al menos dos ramas y dos PR, conservar ocho commits significativos, capturar pipeline rojo/verde, completar evidencias reales, desplegar y publicar el tag `v1.0.0`. Las plantillas no sustituyen evidencia ejecutada.

