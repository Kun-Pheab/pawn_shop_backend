import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

import entities
from database import engine, SessionLocal
import routes.oauth2.controller as auth_controller
import routes.product.controller as product_controller
import routes.client.controller as client_controller
import routes.order.controller as order_controller
import routes.pawn.controller as pawn_controller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("pawn_shop.log")]
)
logger = logging.getLogger(__name__)

# Environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

def create_default_admin():
    """Create a default admin user if none exists."""
    try:
        with SessionLocal() as db:
            from entities import Account
            if db.query(Account).filter(Account.role == "admin").first():
                logger.info("Admin user already exists.")
                return

            from routes.oauth2.repository import create_user
            admin_name = os.getenv("DEFAULT_ADMIN_NAME")
            admin_phone = os.getenv("DEFAULT_ADMIN_PHONE")
            admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD")

            if not all([admin_name, admin_phone, admin_password]):
                logger.error("Missing required admin environment variables.")
                return

            create_user(db, admin_name, admin_phone, admin_password)
            logger.info("Default admin user created successfully.")
    except Exception as e:
        logger.error(f"Failed to create admin user: {str(e)}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    logger.info("Starting Pawn Shop API...")
    try:
        entities.Base.metadata.create_all(engine)
        logger.info("Database tables initialized.")
        create_default_admin()
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
    yield
    logger.info("Shutting down Pawn Shop API...")

app = FastAPI(
    title="Pawn Shop Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"] if ENVIRONMENT == "production" else ["*"],
    expose_headers=["X-Total-Count"] if ENVIRONMENT == "production" else []
)

@app.get("/health", tags=["Health"])
async def health_check():
    """Return API health status."""
    try:
        return {"status": "healthy", "version": "1.0.0"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint for API information."""
    return {"message": "Pawn Shop API", "version": "1.0.0"}

# Include API routers
# app.include_router(auth_controller.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(product_controller.router, prefix="/api/v1/products", tags=["Products"])
# app.include_router(client_controller.router, prefix="/api/v1/clients", tags=["Clients"])
# app.include_router(order_controller.router, prefix="/api/v1/orders", tags=["Orders"])
# app.include_router(pawn_controller.router, prefix="/api/v1/pawn", tags=["Pawn"])

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions."""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=ENVIRONMENT == "development",
        log_level="info"
    )