from fastapi import (
    APIRouter,
    status,
)

router = APIRouter()


@router.get(
    "/health-check",
    tags=["Health check"],
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def health_check():
    """Health check endpoint."""
    return "UP"
