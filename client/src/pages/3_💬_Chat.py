import requests
import streamlit as st

# Установка заголовка и иконки страницы
st.set_page_config(page_title="Chat", page_icon="💬")

# Загрузка изображения бота
st.image("./images/bot.PNG", width=500)

# Заголовок боковой панели
st.sidebar.header("Chat")


def init_page():
    st.set_page_config(page_title="Personal ChatGPT")
    st.header("Personal ChatGPT")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.costs = []


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


def upload_pdf(file):
    upload_url = "http://127.0.0.1:8000/api/v1/upload_pdf/"
    access_token = st.session_state.get("access_token", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    files = {"file": ("filename", file, "application/pdf")}

    response = requests.post(upload_url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()["pdf_paths"]
    else:
        return {"error": "Failed to upload PDF"}


def main():
    # init_page()
    init_messages()

    # Supervise user input
    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(user_input)
        with st.spinner("LLM is typing ..."):
            answer = send_message(st.session_state.messages)
        st.session_state.messages.append(answer)

    # Display chat history
    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, str):
            with st.chat_message("assistant"):
                st.markdown(message)
        elif isinstance(message, str):
            with st.chat_message("user"):
                st.markdown(message)

    # Добавляем выбор файла в sidebar
    uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        # Отправляем загруженный файл и обновляем историю
        upload_response = upload_pdf(uploaded_file)
        st.sidebar.text(f"Upload Response: {upload_response}")


if __name__ == "__main__":
    main()
