import json

import requests
import streamlit as st

sign_in_url = "http://127.0.0.1:8000/api/v1/auth/login"


def signin_form() -> None:
    st.title("Sign In")
    st.header("Please fill out the form to sign in")

    container = st.container(border=True)
    email = container.text_input("Email")
    password = container.text_input("Password")
    input = {"email": email, "password": password}

    if st.button("Sign In"):
        response = requests.post(url=sign_in_url, data=json.dumps(input))
        if response.status_code == 409:  ## already exists
            with st.chat_message(name="assistant"):
                st.write("User not found")

        else:
            with st.chat_message(name="assistant"):
                st.write("User was sign in")
