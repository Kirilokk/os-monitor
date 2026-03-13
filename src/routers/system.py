from fastapi import (
    APIRouter,
    status,
)

from src.services.system_info import get_cpu_info, get_gpu_info

router = APIRouter(prefix="/system")


@router.get(
    "/cpu",
    status_code=status.HTTP_200_OK,
    description="Returns current CPU metrics including usage, cores, and frequency.",
)
def cpu_endpoint():
    return get_cpu_info()


@router.get(
    "/gpu",
    status_code=status.HTTP_200_OK,
    description="Returns current CPU metrics including usage, cores, and frequency.",
)
def gpu_endpoint():
    return get_gpu_info()
