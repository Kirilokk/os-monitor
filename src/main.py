from fastapi import FastAPI

from src.routers.health_check import router as health_check_router
from src.routers.system import router as system_router


def include_routes(application: FastAPI) -> None:
    """Include routers into application."""
    application.include_router(health_check_router)
    application.include_router(system_router)


def get_application() -> FastAPI:
    """Produce and set up FastApi instance."""
    application = FastAPI(
        title="OS monitor",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    include_routes(application)

    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
