import streamlit as st

from src.structures import BatteryData


def show_battery(battery_data: BatteryData):

    if battery_data.power_plugged:
        color = "#16c60c"  # green
        text = "⚡ Charging"
    else:
        color = "#ffb900"  # orange
        text = "🔋 On Battery"

    st.markdown(
        f"""
        <div style="
            padding:15px;
            border-radius:10px;
            background:{color}20;
            border:2px solid {color};
            text-align:center;
            font-size:20px;
        ">
            {text}<br>
            <b>{battery_data.percent:.1f}%</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
