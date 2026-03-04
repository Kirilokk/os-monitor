import streamlit as st


def colored_progress(percent: float):
    if percent > 80:
        color = "#ff4444"
    elif percent > 50:
        color = "#ffaa00"
    else:
        color = "#00cc44"

    st.markdown(
        f"""
        <style>
        .stProgress > div > div > div > div {{
            background-color: {color};
        }}
        </style>
    """,
        unsafe_allow_html=True,
    )
    st.progress(percent / 100)
