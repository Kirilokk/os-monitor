from collections import deque

import streamlit as st
import platform

from src.components.cpu import cpu_block
from src.components.gpu import gpu_block
from src.components.memory import memory_block
from src.components.sensors import sensors_block

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

if "cpu_rows" not in st.session_state:
    st.session_state.cpu_rows = deque(maxlen=120)


st.title("OS Monitor")

with st.container(border=True):
    st.subheader("General information")

    st.markdown(f"""
    Platform: **{platform.system()}**  
    Architecture: **{platform.machine()}**  
    Python version: **{platform.python_version()}**""")


tab_data = [
    ("🧠 CPU", cpu_block),
    ("💾 Memory", memory_block),
    ("🔍 Censors", sensors_block),
]

if platform.system() == "Linux":
    tab_data.insert(1, ("🎮 GPU", gpu_block))

tab_objects = st.tabs([name for name, _ in tab_data])

for tab, (_, handler) in zip(tab_objects, tab_data):
    with tab:
        handler()
