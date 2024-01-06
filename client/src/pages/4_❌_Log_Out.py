import json

import requests
import streamlit as st
from config.settings import settings



log_out_url = settings.log_out_url
st.set_page_config(page_title="Log Out", page_icon="❌")

def click_button():
    st.session_state.clicked = True

st.image("./images/bot.PNG", width=500)
st.sidebar.header("Log Out")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


if st.sidebar.button("Log Out", on_click= click_button):
    access_token = st.session_state.get("access_token", "")
    credentials = {"token":access_token}
    response = requests.post(log_out_url, data = {"credentials":credentials})
    st.sidebar.write(response.json()["detail"])

