import datetime

import pandas as pd
import psutil
import streamlit as st

from src.components.ui.card import card_header, card_body
from src.constants import UPDATE_TIME_IN_SECS


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def cpu_block():
    st.header("CPU data")

    col1, col2, col3 = st.columns([1, 1, 1])
    cols_height = 150

    with col1:
        with st.container(border=True, height=cols_height):
            card_header(
                text="🔢 CPUs cores",
                hover_title="Number of physical/logical cores in the system",
            )
            card_body(
                f"{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}"
            )

    with col2:
        with st.container(border=True, height=cols_height):
            card_header(
                text="🗃️️ Processes",
                hover_title="Total number of running processes on the system",
            )
            card_body(f"{len(psutil.pids())}")

    with col3:
        with st.container(border=True, height=cols_height):
            frequency_now = int(psutil.cpu_freq()[0]) / 1000

            card_header(text="⚙️ Frequency", hover_title="CPU frequency at the moment")
            card_body(f"{frequency_now} GHz")

    st.subheader("CPU Load")

    cpu_times = psutil.cpu_times_percent()
    cpu_dict = cpu_times._asdict()

    # Build a new dictionary with only the needed keys
    needed_keys = ["user", "system", "idle", "nice"]
    cpu_dict = {k: v for k, v in cpu_dict.items() if k in needed_keys}

    cpu_dict["timestamp"] = datetime.datetime.now()
    st.session_state.cpu_rows.append(cpu_dict)

    df = pd.DataFrame(st.session_state.cpu_rows).set_index("timestamp")

    df_plot = df.rename(
        columns={"user": "User", "system": "System", "idle": "Idle", "nice": "Nice"}
    )

    st.dataframe(df_plot, use_container_width=True, height=350)
    st.line_chart(df_plot, x_label="Time", y_label="Load")
