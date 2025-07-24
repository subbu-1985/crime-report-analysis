from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .db import engine, init_db
from .models import Base
from .routes import crimes, maps, chatbot
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AP-Crime-API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup events
    logger.info("Initializing Andhra Pradesh Crime Analytics System")
    await init_db()
    logger.info("Database initialization complete")
    
    yield
    
    # Shutdown events
    logger.info("Shutting down application")

app = FastAPI(
    title="Andhra Pradesh Crime Analytics API",
    description="Real-time crime monitoring and analysis system for AP Police",
    version="1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crimes.router)
app.include_router(maps.router)
app.include_router(chatbot.router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected" if engine else "disconnected",
        "environment": settings.ENVIRONMENT
    }
