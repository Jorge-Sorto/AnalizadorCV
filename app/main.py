from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import get_settings
from app.services.analyzer import AnalyzerService
from app.services.llm_client import DemoLLMClient, OpenAILLMClient


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version, docs_url="/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    if settings.llm_provider == "openai" and settings.openai_api_key:
        client = OpenAILLMClient(settings.openai_api_key, settings.openai_model, settings.llm_timeout_seconds)
    else:
        client = DemoLLMClient()
    app.state.analyzer = AnalyzerService(client)
    app.include_router(router)
    static = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=static), name="static")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(static / "index.html")

    return app


app = create_app()
