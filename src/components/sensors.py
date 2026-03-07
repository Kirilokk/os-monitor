import time
import psutil
import streamlit as st

from src.components.ui.sensors import show_battery
from src.constants import UPDATE_TIME_IN_SECS
from src.utils import detect_temperature_sensors, get_all_temperatures


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def censors_block():
    st.header("Censors data")

    uptime = int(time.time() - psutil.boot_time())

    hours = uptime // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60

    st.metric("⏱ Uptime", f"{hours:02}:{minutes:02}:{seconds:02}")

    # st.write(psutil.sensors_temperatures())
    sensor_map = detect_temperature_sensors()
    temps = get_all_temperatures(sensor_map)

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

    st.subheader("🔋 Battery")

    battery = psutil.sensors_battery()
    if battery:
        show_battery(battery_data=battery)
