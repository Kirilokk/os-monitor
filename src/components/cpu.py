import datetime

import pandas as pd
import streamlit as st

from src.services.system_info import get_cpu_info
from src.components.ui.card import card_header, card_body
from src.constants import UPDATE_TIME_IN_SECS


@st.fragment(run_every=UPDATE_TIME_IN_SECS)
def cpu_block():
    st.header("CPU data")

    col1, col2, col3 = st.columns([1, 1, 1])
    cols_height = 150

    cpu_data = get_cpu_info()

    with col1:
        with st.container(border=True, height=cols_height):
            card_header(
                text="🔢 CPUs cores",
                hover_title="Number of physical/logical cores in the system",
            )
            card_body(f"{cpu_data.physical_count}/{cpu_data.logical_count}")

    with col2:
        with st.container(border=True, height=cols_height):
            card_header(
                text="🗃️️ Processes",
                hover_title="Total number of running processes on the system",
            )
            card_body(f"{len(cpu_data.process_ids)}")

    with col3:
        with st.container(border=True, height=cols_height):
            frequency_now = int(cpu_data.frequency) / 1000

            card_header(text="⚙️ Frequency", hover_title="CPU frequency at the moment")
            card_body(f"{frequency_now} GHz")

    st.subheader("CPU Load")

    # Build a new dictionary with only the needed keys
    needed_keys = ["user", "system", "idle"]
    cpu_dict = {k: v for k, v in cpu_data.usage.items() if k in needed_keys}

    cpu_dict["timestamp"] = datetime.datetime.now()
    st.session_state.cpu_rows.append(cpu_dict)

    df = pd.DataFrame(st.session_state.cpu_rows).set_index("timestamp")

    df_plot = df.rename(columns={"user": "User", "system": "System", "idle": "Idle"})

    st.dataframe(df_plot, use_container_width=True, height=350)
    st.line_chart(df_plot, x_label="Time", y_label="Load")
