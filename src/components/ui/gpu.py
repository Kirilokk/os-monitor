import streamlit as st

from src.components.ui.charts import build_vram_chart
from src.structures import GPUInfo, GpuType
from src.utils import get_gpu_metrics


def single_gpu_block(key: int, gpu: GPUInfo) -> None:
    load, vram_used, vram_total, vram_percent = get_gpu_metrics(gpu)
    gpu_type_label = (
        "🧠 Integrated" if gpu.type == GpuType.INTEGRATED else "⚡ Discrete"
    )

    with st.container():
        st.markdown(
            f'<div class="title">🎮 {gpu.name} <span style="font-size:16px;color:gray">({gpu_type_label})</span></div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("GPU Load", f"{load}%")
            st.progress(load / 100)
            st.metric("Temperature", f"{gpu.temperature} °C")
            st.metric("Power Usage", f"{gpu.power_usage_watts} W")

        with col2:
            fig = build_vram_chart(vram_used, vram_total, vram_percent)

            st.plotly_chart(fig, use_container_width=True, key=key)

            st.write(f"**VRAM Used:** {vram_used:.2f} GB")
            st.write(f"**Total VRAM:** {vram_total:.2f} GB")
