from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routes.chat import (
    memory_router,
    router as chat_router,
)


app = FastAPI(
    title="AI Memory Companion API",
    description="Backend API for the AI Memory Companion",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(memory_router)


@app.get("/")
async def root():
    return {
        "message": "AI Memory Companion API is running",
        "phase": "Phase 2 - Long-Term Memory",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }