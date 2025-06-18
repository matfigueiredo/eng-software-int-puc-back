import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from core.lifespan import lifespan
from logger import setup_logger
from routers import prediction

# Setup logger
setup_logger()

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)