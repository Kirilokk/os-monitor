import time

import psutil
from pyamdgpuinfo import GPUInfo, get_gpu
from src.utils import (
    detect_temperature_sensors,
    get_all_temperatures,
    get_battery_status,
)
from src.structures import CPUInfo, MemoryInfo, BatteryData, SensorsData


def get_cpu_info():
    return CPUInfo(
        physical_count=psutil.cpu_count(logical=False),
        logical_count=psutil.cpu_count(logical=True),
        frequency=psutil.cpu_freq()[0],
        process_ids=psutil.pids(),
        usage=psutil.cpu_times_percent()._asdict(),
    )


def get_gpu_info() -> GPUInfo:
    return get_gpu(0)


def get_memory_info() -> MemoryInfo:
    storage_memory = psutil.disk_usage("/")
    virtual_memory = psutil.virtual_memory()

    return MemoryInfo(
        total_storage_bytes=storage_memory.total,
        used_storage_bytes=storage_memory.used,
        total_virtual_memory_bytes=virtual_memory.total,
        used_virtual_memory_bytes=virtual_memory.used,
    )


def get_sensors_data():
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
