import streamlit as st


def side_bar() -> None:
    with st.sidebar:
        button = st.button("Sign Up")
        if button:
            st.session_state["form"] = "register"
        button = st.button("Sign In")
        if button:
            st.session_state["form"] = "login"
