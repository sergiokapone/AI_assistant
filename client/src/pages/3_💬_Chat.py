import requests
import streamlit as st
from config.settings import settings
from streamlit.runtime.uploaded_file_manager import UploadedFile

# Установка заголовка и иконки страницы
st.set_page_config(page_title="Chat", page_icon="💬")

# Загрузка изображения бота
st.image("./images/bot.PNG", width=500)

# Заголовок боковой панели
st.sidebar.header("Chat")


def send_message(message):
    chat_url = settings.chat_url
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


def upload_file(
    uploaded_file: UploadedFile,
) -> requests.Response:
    upload_url = settings.uload_file_url
    access_token = st.session_state.get("access_token", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    file_name: str = uploaded_file.name

    files = {"file": (file_name, uploaded_file)}

    response = requests.post(
        upload_url,
        files=files,
        headers=headers,
    )

 
    if response.status_code == 200:
        return {"message": "File uploaded successfully", "response": response.json()}
    else:
        return {"error": "Failed to upload PDF", "response": response.json()}


def select_llm(llm_model: str) -> requests.Response:
    selector_url = settings.llm_selector_url
    access_token = st.session_state.get("access_token", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "llm_name": f"{llm_model}",
    }
    response = requests.post(selector_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["message"]
    else:
        return "Failed to upload LLM: possible reason not authorized"


def get_message_history():
    get_user_by_email_url = settings.get_history_url
    access_token = st.session_state.get("access_token", "")
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.get(get_user_by_email_url, headers=headers)
    if response.status_code == 200:
        return response.json()["history"]
    else:
        return "Failed to retrieve the message history"


def clear_messages_btn():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button:
        st.session_state.messages = []


def retrive_messages_btn(avatar):
    if st.sidebar.button("Retrieve chat history."):
        retrive_messages(avatar)


def retrive_messages(avatar):
    message_history = get_message_history()
    if "messages" in st.session_state:
        for message in message_history:
            st.session_state.messages.append({"role": "user", "content": message[0]})
            with st.chat_message("user", avatar=avatar["user"]):
                st.markdown(message[0])
            with st.chat_message("assistant", avatar=avatar["assistant"]):
                st.markdown(message[1])
            st.session_state.messages.append(
                {"role": "assistant", "content": message[1]}
            )


def upload_file_btn():
    #    uploaded_file = st.sidebar.file_uploader("Upload File", type=["pdf", "txt", "docx"])
    # if uploaded_file and not st.session_state.get("file_uploaded", False):
    #     st.session_state.file_uploaded = True
    #     upload_file(uploaded_file)

    if uploaded_file := st.sidebar.file_uploader(
        "Upload File", type=["pdf", "txt", "docx"]
    ):
        upload_file(uploaded_file)



def select_llm_el():
    option = st.sidebar.selectbox(
        "Please select LLM model to communicate with.", settings.LLM_MODELS
    )
    select_llm(option)


def session_init():

    # st.session_state.messages = []
    # retrive_messages(avatar)

    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():
    avatar = {"user": "./images/human.png", "assistant": "./images/logo.PNG"}

    if "email" not in st.session_state:
        with st.chat_message("assistant", avatar=avatar["assistant"]):
            st.write("You are not authenticated. Please sign in.")
        return

    user_email = st.session_state.email

    session_init()

    clear_messages_btn()
    retrive_messages_btn(avatar)

    upload_file_btn()
    select_llm_el()

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=avatar[message["role"]]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"{user_email} Ask question here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatar["user"]):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatar["assistant"]):
            message_placeholder = st.empty()
        with st.spinner("LLM is typing ..."):
            answer = send_message(prompt)
            message_placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
