import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import platform
import psutil
import datetime

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
    st.header("CPU data")

    col1, col2, col3 = st.columns([1, 1, 1])
    cols_height = 150

    with col1:
        with st.container(border=True, height=cols_height):
            st.markdown("#### 🔢 Logical CPUs")

            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 28px;
                ">
                    {psutil.cpu_count()}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        with st.container(border=True, height=cols_height):
            st.markdown("#### 🗃️️ Processes",    help="Total number of running processes on the system")

            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 28px;
                ">
                    {len(psutil.pids())}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        with st.container(border=True, height=cols_height):
            frequency_now = int(psutil.cpu_freq()[0]) / 1000

            st.markdown("#### ⚙️ Frequency")
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 28px;
                ">
                    {frequency_now} GHz
                </div>
                """,
                unsafe_allow_html=True
            )

    st.subheader('Load')

    cpu_times = psutil.cpu_times_percent()
    cpu_dict = cpu_times._asdict()
    cpu_dict["timestamp"] = datetime.datetime.now()

    st.session_state.cpu_rows.append(cpu_dict)

    if len(st.session_state.cpu_rows) > 120:
        st.session_state.cpu_rows.pop(0)

    df = pd.DataFrame(st.session_state.cpu_rows)
    df = df.set_index("timestamp")
    st.dataframe(df, use_container_width=True, height=350)

    st.line_chart(df)

with tab2:
    st.header("Memory data")
with tab3:
    st.header("Networks data")
