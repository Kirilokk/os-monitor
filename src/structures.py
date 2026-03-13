from dataclasses import dataclass


@dataclass
class CPUInfo:
    physical_count: int
    logical_count: int
    frequency: int
    process_ids: list[int]
    usage: dict


@dataclass
class MemoryInfo:
    total_storage_bytes: int
    used_storage_bytes: int
    total_virtual_memory_bytes: int
    used_virtual_memory_bytes: int


@dataclass
class BatteryData:
    percent: float | None
    power_plugged: bool | None


@dataclass
class SensorsData:
    temperatures: dict
    boot_time: float
    battery: BatteryData | None
