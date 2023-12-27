# app.py

import streamlit as st


def main():
    st.title("Пример приложения с Streamlit")

    # Добавление виджетов
    name = st.text_input("Введите ваше имя", "Имя")
    submit_button = st.button("Отправить")

    # Обработка событий
    if submit_button:
        st.write(f"Привет, {name}!")


if __name__ == "__main__":
    main()
