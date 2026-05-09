from fastapi import FastAPI

from app.api.routes import router
from app.utils.config_loader import settings
from app.observability.logger import logger


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.include_router(router)


@app.on_event("startup")
async def startup_event():

    logger.info(
        "application_startup",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


@app.on_event("shutdown")
async def shutdown_event():

    logger.info(
        "application_shutdown"
    )