import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import platform
import psutil
import datetime

if "rows" not in st.session_state:
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
    st.header("CPU data")

    cpu_times = psutil.cpu_times_percent()
    cpu_dict = cpu_times._asdict()

    cpu_dict["timestamp"] = datetime.datetime.now()

    st.session_state.rows.append(cpu_dict)

    if len(st.session_state.rows) > 120:
        st.session_state.rows.pop(0)

    df = pd.DataFrame(st.session_state.rows)
    df = df.set_index("timestamp")
    st.dataframe(df, use_container_width=True)

    st.line_chart(df)

with tab2:
    st.header("Memory data")
with tab3:
    st.header("Networks data")
