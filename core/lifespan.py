from contextlib import asynccontextmanager

from fastapi import FastAPI

from logger import log_info
from services.prediction_service import prediction_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    log_info("🚀 Starting up...")
    prediction_service.load_model()
    
    yield
    
    # Shutdown
    log_info("�� Shutting down...") 