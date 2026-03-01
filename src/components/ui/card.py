import streamlit as st


def card_header(text: str, hover_title=None):
    tip_attr = hover_title if hover_title else ""
    st.markdown(
        f"""
        <h4 style="
            text-align: center;
            white-space: nowrap;
        " title="{tip_attr}">
            {text}
        </h4>
        """,
        unsafe_allow_html=True,
    )


def card_body(text: str):
    st.markdown(
        f"""
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 28px;
                    ">
                        {text}
                    </div>
                    """,
        unsafe_allow_html=True,
    )
