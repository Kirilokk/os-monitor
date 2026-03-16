from fastapi import (
    APIRouter,
)
from starlette.exceptions import HTTPException

from src.services.system_info import (
    get_cpu_info,
    get_gpu_info,
    get_memory_info,
    get_sensors_data,
)
from src.structures import SensorsData, CPUInfo, GPUInfo, MemoryInfo

router = APIRouter(prefix="/system")


@router.get(
    "/cpu",
    description="Returns current CPU metrics including usage, cores, and frequency.",
    response_model=CPUInfo,
)
def cpu_endpoint() -> CPUInfo:
    return get_cpu_info()


@router.get(
    "/gpu",
    description="Returns current GPUs metrics including load, temperature, memory usage, and power consumption.",
    response_model=list[GPUInfo],
)
def gpu_endpoint() -> list[GPUInfo]:
    gpu = get_gpu_info()

    if gpu is None:
        raise HTTPException(404, "GPU not available")

    return gpu


@router.get(
    "/memory",
    description="Returns current storage and virtual memory usage.",
    response_model=MemoryInfo,
)
def memory_endpoint():
    return get_memory_info()


@router.get(
    "/sensors",
    description="Returns current sensors metrics including temperatures for main components, boot time and battery status",
    response_model=SensorsData,
)
def sensors_endpoint():
    return get_sensors_data()
