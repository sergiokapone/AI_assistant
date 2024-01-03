import json

import requests
import streamlit as st

sign_up_url = "http://127.0.0.1:8000/api/v1/auth/signup"
USER_EXIST = "Email already exists"


def signup_form() -> None:
    st.set_page_config(page_title="Sign Up", page_icon="✏️")

    st.image("./images/bot.PNG", width=500)
    st.header("Please fill out the form to sign up")
    st.markdown("# Sign Up")
    st.sidebar.header("Sign Up")

    container = st.container(border=True)
    email = container.text_input("Email")
    password = container.text_input("Password")
    username = container.text_input("Username")
    input = {"email": email, "password": password, "username": username}

    if st.button("Sign Up"):
        response = requests.post(url=sign_up_url, data=json.dumps(input))
        if response.status_code == 409:  ## already exists
            with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                st.write("User already registered. Please use Sign In page.")
        elif response.status_code == 422:  ## unprocessable entity
            with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                st.write("Incorrect form.")
        else:
            with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                st.write("User was succefully created.")

if __name__ == "__main__":
    signup_form()
