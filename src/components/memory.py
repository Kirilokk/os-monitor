import streamlit as st
from matplotlib import pyplot as plt

from src.services.system_info import get_memory_info
from src.components.ui.card import card_header, card_body
from src.components.ui.progress_bar import colored_progress
from src.constants import BYTES_IN_GB, UPDATE_TIME_IN_SECS


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def memory_block():
    st.header("Memory data")

    col1, col2, col3 = st.columns([1, 1, 1])
    cols_height = 150

    memory_data = get_memory_info()
    total = memory_data.total_storage_bytes / BYTES_IN_GB
    used = memory_data.used_storage_bytes / BYTES_IN_GB
    free = total - used

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

    total_virtual_memory = memory_data.total_virtual_memory_bytes / BYTES_IN_GB
    used_virtual_memory = memory_data.used_virtual_memory_bytes / BYTES_IN_GB

    colored_progress(percent=(used_virtual_memory / total_virtual_memory) * 100)
    st.write(
        f"Used: {used_virtual_memory:.2f} GB / Total: {total_virtual_memory:.2f} GB"
    )
