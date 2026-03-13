import streamlit as st
import plotly.graph_objects as go

from src.services.system_info import get_gpu_info
from src.constants import BYTES_IN_GB, UPDATE_TIME_IN_SECS
from src.utils import gpu_available


def gpu_block():
    if gpu_available():
        show_gpu_metrics()
    else:
        st.info("🖥 GPU metrics are not available in this environment.")


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def show_gpu_metrics():

    gpu = get_gpu_info()

    load = int(gpu.query_load() * 100)
    vram_used = gpu.query_vram_usage() / BYTES_IN_GB
    vram_total = gpu.memory_info["vram_size"] / BYTES_IN_GB
    vram_percent = (vram_used / vram_total) * 100

    st.markdown(
        """
    <style>

    .title {
        font-size: 28px;
        font-weight: 700;
        text-align:center;
        margin-bottom:15px;
    }

    .metric {
        font-size: 18px;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(f'<div class="title">🎮 {gpu.name}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # LEFT SIDE
        with col1:
            st.metric("GPU Load", f"{load}%")
            st.progress(load / 100)
            st.metric("Temperature", f"{gpu.query_temperature()} °C")
            st.metric("Power Usage", f"{gpu.query_power()} W")

        # RIGHT SIDE
        with col2:
            fig = go.Figure(
                go.Pie(
                    values=[vram_used, vram_total - vram_used],
                    labels=["Used", "Free"],
                    hole=0.65,
                    textinfo="none",
                )
            )

            fig.update_layout(
                height=250,
                margin=dict(t=0, b=0, l=0, r=0),
                annotations=[
                    dict(text=f"{vram_percent:.0f}%", showarrow=False, font_size=28)
                ],
            )

            st.plotly_chart(fig, use_container_width=True)

            st.write(f"**VRAM Used:** {vram_used:.2f} GB")
            st.write(f"**Total VRAM:** {vram_total:.2f} GB")
