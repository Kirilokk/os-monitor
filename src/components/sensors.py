import time
import psutil
import streamlit as st

from src.components.ui.sensors import show_battery
from src.constants import UPDATE_TIME_IN_SECS
from src.utils import detect_temperature_sensors, get_all_temperatures, get_battery_status


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def censors_block():
    st.header("Censors data")

    uptime = int(time.time() - psutil.boot_time())

    hours = uptime // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60

    st.metric("⏱ Uptime", f"{hours:02}:{minutes:02}:{seconds:02}")


    sensor_map = detect_temperature_sensors()
    temps = get_all_temperatures(sensor_map)

    if all(value is None for value in temps.values()):
        st.info("🌡 Temperature metrics are not available in this environment.")
    else:
        show_temperatures(temps)


    battery = get_battery_status()
    if battery:
        st.subheader("🔋 Battery")
        show_battery(battery_data=battery)
    else:
        st.info("🔋 Battery info not available in this environment")


def show_temperatures(temps):
    with st.container(border=True):
        st.subheader("Temperatures")
        cols = st.columns(2)

        # Place metrics in columns
        cols[0].metric("CPU 🌡️", f"{temps['cpu']:.1f} °C")
        cols[1].metric("GPU 🌡️", f"{temps['gpu']:.1f} °C")

        # Next row
        cols = st.columns(2)
        cols[0].metric("RAM 🌡️", f"{temps['ram']:.1f} °C")
        cols[1].metric("SSD 🌡️", f"{temps['disk']:.1f} °C")
