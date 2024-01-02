import streamlit as st
from components import signin, signup


def show_form(form_type):
    if form_type == "SIGN UP":
        signup.signup_form()

    elif form_type == "SIGN IN":
        signin.signin_form()


# Заголовок боковой панели
st.sidebar.title("Select Option")

# Создание боковой панели с кнопками "Sign In" и "Sign Up"
selected_action = st.sidebar.radio("", ["SIGN UP", "SIGN IN"])

# Отображение формы в основном окне при выборе действия


if __name__ == "__main__":
    show_form(selected_action)


