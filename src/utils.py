import os

import psutil


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

    return {
        name: get_temperature(temps, chip, label) if chip else None
        for name, (chip, label) in sensor_map.items()
        if chip
    }
