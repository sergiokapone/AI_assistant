import requests
import streamlit as st
from streamlit_chat import message

# Установка заголовка и иконки страницы
st.set_page_config(page_title="Chat", page_icon="💬")

# Загрузка изображения бота
st.image("./images/bot.PNG", width=500)

# Заголовок боковой панели
st.sidebar.header("Chat")


# Функция отправки сообщения на сервер и получения ответа
def send_message(message):
    chat_url = "http://127.0.0.1:8000/api/v1/chat/"
    access_token = st.session_state.get("access_token", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"user_query": message}

    response = requests.post(chat_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["string"]
    else:
        return {"error": "Failed to send message"}


# Основная функция
def main():
    # Заголовок страницы
    st.title("Chat with Backend")

    # Создание контейнеров для ввода и отображения ответов
    response_container = st.container()
    text_container = st.container()

    # Инициализация переменных
    details = ""

    if "responses" not in st.session_state:
        st.session_state["responses"] = ["I'm here to assist you!"]

    if "requests" not in st.session_state:
        st.session_state["requests"] = []

    if "buffer_memory" not in st.session_state:
        st.session_state.buffer_memory = ""

    # Ввод пользователя и кнопка отправки
    with text_container:
        query = st.text_input("You:", key="input", placeholder="Start chat")
        submit = st.button("Send")

        if submit:
            response = send_message(query)
            st.session_state.requests.append(query)
            st.session_state.responses.append(response)

    # Отображение ответов
    with response_container:
        if st.session_state["responses"]:
            for i in range(len(st.session_state["responses"])):
                message(
                    st.session_state["responses"][i],
                    key=str(i),
                    avatar_style="no-avatar",
                    allow_html=True,
                )
                if i < len(st.session_state["requests"]):
                    message(
                        st.session_state["requests"][i],
                        is_user=True,
                        key=str(i) + "_user",
                        allow_html=True,
                    )


if __name__ == "__main__":
    main()
