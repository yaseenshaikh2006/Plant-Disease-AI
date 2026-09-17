"""
FastAPI Application Entry Point
Plant Disease AI – Plant Disease Prediction & Smart Recommendation System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import router
from app.core.config import MODELS_DIR

app = FastAPI(
    title="Plant Disease AI API",
    description="Deep Learning Plant Disease Diagnosis and Agronomic Recommendation Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount evaluation artifacts / plots directory if available
if MODELS_DIR.exists():
    app.mount("/static/models", StaticFiles(directory=str(MODELS_DIR)), name="model_plots")

# Include routes both at /api and at root for full endpoint compatibility
app.include_router(router, prefix="/api")
app.include_router(router, prefix="")


@app.get("/")
def root():
    return {
        "title": "Plant Disease AI – Plant Disease Prediction & Smart Recommendation System",
        "endpoints": {
            "predict": "POST /predict or POST /api/predict",
            "health": "GET /health or GET /api/health",
            "crops": "GET /api/crops",
            "diseases": "GET /api/diseases",
            "evaluation": "GET /api/evaluation",
            "docs": "GET /docs"
        },
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
