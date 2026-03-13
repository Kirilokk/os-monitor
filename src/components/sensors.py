import streamlit as st

from src.services.system_info import get_sensors_data
from src.components.ui.sensors import show_battery
from src.constants import UPDATE_TIME_IN_SECS


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def sensors_block():
    st.header("Sensors data")

    sensors_data = get_sensors_data()

    hours = sensors_data.boot_time // 3600
    minutes = (sensors_data.boot_time % 3600) // 60
    seconds = sensors_data.boot_time % 60

    st.metric("⏱ Uptime", f"{hours:02}:{minutes:02}:{seconds:02}")

    # TODO: test sensors
    temps = sensors_data.temperatures

    if all(value is None for value in temps.values()):
        st.info("🌡 Temperature metrics are not available in this environment.")
    else:
        show_temperatures(temps)

    if sensors_data.battery:
        st.subheader("🔋 Battery")
        show_battery(battery_data=sensors_data.battery)
    else:
        st.info("🔋 Battery info not available in this environment")

    # TODO: check fans


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
