import os

import psutil

from src.constants import BYTES_IN_GB
from src.structures import GpuType


def gpu_available() -> bool:
    return os.path.exists("/dev/dri")


def get_temperature(temps, chip, label=None):
    sensors = temps.get(chip, [])

    for sensor in sensors:
        if label and sensor.label != label:
            continue
        if sensor.current is not None:
            return sensor.current

    return None


def detect_temperature_sensors():
    temps = psutil.sensors_temperatures()

    mapping = {
        "cpu": None,
        "gpu": None,
        "disk": None,
        "ram": None,
    }

    for chip, sensors in temps.items():
        # CPU
        if chip in ("k10temp", "coretemp"):
            mapping["cpu"] = (chip, "Tctl")

        # GPU
        elif chip in ("amdgpu", "nouveau"):
            mapping["gpu"] = (chip, None)

        # NVMe SSD
        elif chip == "nvme":
            mapping["disk"] = (chip, "Composite")

        # RAM sensors
        elif chip.startswith("spd"):
            mapping["ram"] = (chip, None)

    return mapping


def get_all_temperatures(sensor_map):
    temps = psutil.sensors_temperatures()

    result = {}
    for name, value in sensor_map.items():
        if value is None:
            result[name] = None
            continue

        chip, label = value
        result[name] = get_temperature(temps, chip, label)

    return result


def get_gpu_metrics(gpu):
    load = int(gpu.load * 100)

    vram_used = gpu.used_virtual_memory_bytes / BYTES_IN_GB
    vram_total = gpu.total_virtual_memory_bytes / BYTES_IN_GB
    vram_percent = (vram_used / vram_total) * 100 if vram_total else 0

    return load, vram_used, vram_total, vram_percent


def get_battery_status():
    try:
        return psutil.sensors_battery()
    except FileNotFoundError:
        return None


def get_gpu_type(vram_bytes: int) -> GpuType:
    if vram_bytes >= 4 * BYTES_IN_GB:
        return GpuType.DISCRETE
    else:
        return GpuType.INTEGRATED
