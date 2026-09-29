from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="AI-powered fitness plan generator using Google Gemini",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "application": "FitBuddy"
    }
