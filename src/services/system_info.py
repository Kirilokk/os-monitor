import time

import psutil
from pyamdgpuinfo import get_gpu, detect_gpus

from src.utils import (
    detect_temperature_sensors,
    get_all_temperatures,
    get_battery_status,
)
from src.structures import CPUInfo, MemoryInfo, BatteryData, SensorsData, GPUInfo
from src.utils import get_gpu_type
from src.structures import GpuType


def get_cpu_info():
    return CPUInfo(
        physical_count=psutil.cpu_count(logical=False),
        logical_count=psutil.cpu_count(logical=True),
        frequency=psutil.cpu_freq()[0],
        usage=psutil.cpu_times_percent()._asdict(),
        process_ids=psutil.pids(),
    )


def get_gpu_info() -> list[GPUInfo] | None:
    try:
        gpus = [get_gpu(x) for x in range(detect_gpus())]
    except (RuntimeError, OSError):
        return None

    gpus_info = [
        GPUInfo(
            name=gpu.name,
            load=gpu.query_load(),
            total_virtual_memory_bytes=gpu.memory_info["vram_size"],
            used_virtual_memory_bytes=gpu.query_vram_usage(),
            temperature=gpu.query_temperature(),
            power_usage_watts=gpu.query_power(),
            type=get_gpu_type(vram_bytes=gpu.query_vram_usage()),
        )
        for gpu in gpus
    ]

    # Return sorted GPUs with discrete always at the top
    return sorted(gpus_info, key=lambda gpu: gpu.type == GpuType.INTEGRATED)


def get_memory_info() -> MemoryInfo:
    storage_memory = psutil.disk_usage("/")
    virtual_memory = psutil.virtual_memory()

    return MemoryInfo(
        total_storage_bytes=storage_memory.total,
        used_storage_bytes=storage_memory.used,
        total_virtual_memory_bytes=virtual_memory.total,
        used_virtual_memory_bytes=virtual_memory.used,
    )


def get_sensors_data() -> SensorsData:
    sensor_map = detect_temperature_sensors()
    temperatures = get_all_temperatures(sensor_map)

    # Battery
    battery_data = None
    battery = get_battery_status()
    if battery is not None:
        battery_data = BatteryData(
            percent=getattr(battery, "percent", None),
            power_plugged=getattr(battery, "power_plugged", None),
        )
        if battery_data.percent is None and battery_data.power_plugged is None:
            battery_data = None

    return SensorsData(
        temperatures=temperatures,
        boot_time=int(time.time() - psutil.boot_time()),
        battery=battery_data,
    )
