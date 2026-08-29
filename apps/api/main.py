from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Memory Companion API",
    description="Backend API for the AI Memory Companion",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "AI Memory Companion API is running",
        "phase": "Phase 1 - Basic Conversational AI",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }