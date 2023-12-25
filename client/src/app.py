import streamlit as st

# Заголовок формы
st.title("Пример формы в Streamlit")

def click_handler():
    st.write("I'm clicked")


st.button("Click here!", on_click=click_handler)

