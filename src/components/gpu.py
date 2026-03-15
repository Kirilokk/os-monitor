import streamlit as st

from src.components.ui.gpu import single_gpu_block
from src.structures import GPUInfo
from src.services.system_info import get_gpu_info
from src.constants import UPDATE_TIME_IN_SECS
from src.utils import gpu_available


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def gpu_block():
    gpu_data = get_gpu_info()
    if gpu_available() and gpu_data:
        show_gpu_metrics(gpu_data)
    else:
        st.info("🖥 GPU metrics are not available in this environment.")


def show_gpu_metrics(gpus: list[GPUInfo]):
    for index, gpu in enumerate(gpus):
        single_gpu_block(key=index, gpu=gpu)
        st.divider()
