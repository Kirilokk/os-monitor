import streamlit as st
from streamlit_autorefresh import st_autorefresh
import platform

from src.components.cpu import cpu_block
from src.components.memory import memory_block

if "cpu_rows" not in st.session_state:
    st.session_state.cpu_rows = []

st_autorefresh(interval=1000, key="cpu_refresh")


st.title("OS Monitor")

with st.container(border=True):
    st.subheader("General information")

    st.markdown(f"""
    Platform: **{platform.system()}**  
    Architecture: **{platform.machine()}**  
    Python version: **{platform.python_version()}**""")


tab1, tab2, tab3 = st.tabs(["🧠 CPU", "💾 Memory", "🌐 Networks"])

with tab1:
    cpu_block()

with tab2:
    memory_block()
with tab3:
    st.header("Networks data")
