import requests
import streamlit as st
from config.settings import settings

log_out_url = settings.log_out_url
##print(log_out_url)
st.set_page_config(page_title="Log Out", page_icon="❌")


def click_button():
    st.session_state.clicked = True


st.image("./images/bot.PNG", width=500)
st.sidebar.header("Log Out")

if "clicked" not in st.session_state:
    st.session_state.clicked = False

avatar = {"user": "./images/human.png", "assistant": "./images/logo.PNG"}

if "messages" in st.session_state:
    st.session_state.messages = []

if "email" in st.session_state:
    if st.sidebar.button("Log Out", on_click=click_button):
        access_token = st.session_state.get("access_token", "")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"credentials": access_token}
        response = requests.post(log_out_url, headers=headers, data=data)
        st.sidebar.write(response.json()["message"])
        if response.status_code == 200:
            del st.session_state["email"]
else:
    with st.chat_message("assistant", avatar=avatar["assistant"]):
        st.write("You are not authenticated. Please sign in.")
