from collections import deque

import streamlit as st
import platform

from src.components.cpu import cpu_block
from src.components.gpu import gpu_block
from src.components.memory import memory_block
from src.components.sensors import censors_block

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
    ("🔍 Censors", censors_block),
]

if platform.system() == "Linux":
    tab_data.insert(1, ("🎮 GPU", gpu_block))

tab_objects = st.tabs([name for name, _ in tab_data])

for tab, (_, handler) in zip(tab_objects, tab_data):
    with tab:
        handler()
