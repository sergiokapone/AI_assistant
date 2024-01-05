import requests
import streamlit as st
from config.settings import settings


def signin_form() -> None:
    sign_in_url = settings.sign_in_url
    st.set_page_config(page_title="Sign In", page_icon="🗝️")
    st.image("./images/bot.PNG", width=500)
    st.header("Please fill out the form to sign in")
    st.markdown("# Sign In")
    st.sidebar.header("Sign In")

    container = st.container(border=True)
    email = container.text_input("Email ")
    password = container.text_input("Password ", type="password")
    input = {"username": email, "password": password}

    if st.button("Sign In"):
        try:
            response = requests.post(url=sign_in_url, data=input)
            response_data = response.json()  # Парсим JSON-ответ
            access_token = response_data.get("access_token")

            if access_token:
                # Зберігаємо токен у session_state
                st.session_state.access_token = access_token

                # Виводимо інформацію про успішну аутентифікацію
                with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                    st.write("User was signed in successfully.")

            else:
                # Виводимо інформацію про помилку аутентифікації
                with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                    st.write("User not found or incorrect credentials.")

        except ConnectionRefusedError:
            with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                st.write("No connection with the server.")


if __name__ == "__main__":
    signin_form()
