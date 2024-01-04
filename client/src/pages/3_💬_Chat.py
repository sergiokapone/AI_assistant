import requests
import streamlit as st

st.set_page_config(page_title="Chat", page_icon="💬")
st.image("./images/bot.PNG", width=500)
st.sidebar.header("Chat")


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


def main():
    st.title("Chat with Backend")

    user_input = st.text_input("Enter your message:")
    if st.button("Send"):
        if user_input:
            response = send_message(user_input)
            st.text("Server Response:")
            st.text(response)


if __name__ == "__main__":
    main()
