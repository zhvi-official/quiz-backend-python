from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from features.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from core.logger import logger

    logger.info("Pydantic models rebuilded.")
    yield


app = FastAPI(title="Home file sharing", docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json", swagger_ui_oauth2_redirect_url="/api/docs/oauth2-redirect", lifespan=lifespan)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def root():
    return "Hello, this is a web service for quiz."
