

from fastapi import FastAPI
from GigaAmService.app.api.router import router as transcription_router

app = FastAPI(
    title="Transcription Service API",
    description="API для транскрипции аудио с использованием GigaAM.",
    version="1.0.0"
)

app.include_router(transcription_router, prefix="/api/v1", tags=["Transcription"])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok"}