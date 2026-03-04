import psutil
import streamlit as st
from matplotlib import pyplot as plt

from src.components.ui.card import card_header, card_body
from src.components.ui.progress_bar import colored_progress
from src.constants import BYTES_IN_GB


def memory_block():
    st.header("Memory data")

    col1, col2, col3 = st.columns([1, 1, 1])
    cols_height = 150

    disk = psutil.disk_usage("/")
    total = disk.total / BYTES_IN_GB
    used = disk.used / BYTES_IN_GB
    free = disk.free / BYTES_IN_GB

    with col1:
        with st.container(border=True, height=cols_height):
            card_header(
                text="📦 Total",
                hover_title="Total disk space",
            )
            card_body(f"{total:.2f} GB")
    with col2:
        with st.container(border=True, height=cols_height):
            card_header(
                text="🟢 Free",
                hover_title="Free disk space. May differ due to reserved filesystem blocks and metadata.",
            )
            card_body(f"{free:.2f} GB")

    with col3:
        with st.container(border=True, height=cols_height):
            card_header(
                text="🔴 Used",
                hover_title="Used disk space. Includes filesystem overhead and reserved space.",
            )
            card_body(f"{used:.2f} GB")

    st.subheader("Disk usage")
    fig, ax = plt.subplots(figsize=(3, 3))

    ax.pie(
        [used, free],
        explode=(0, 0.1),
        autopct="%1.1f%%",
        colors=["xkcd:bright yellow", "xkcd:sky blue"],
        shadow=True,
        startangle=150,
        labels=["Used", "Free"],
        textprops={"fontsize": 8},
    )
    ax.axis("equal")

    st.pyplot(fig, use_container_width=False)

    st.subheader("RAM in real time")

    ram_memory = psutil.virtual_memory()

    colored_progress(percent=ram_memory.percent)
    st.write(
        f"Used: {ram_memory.used / BYTES_IN_GB:.2f} GB / Total: {ram_memory.total / BYTES_IN_GB:.2f} GB"
    )
