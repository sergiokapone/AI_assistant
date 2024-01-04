import requests
import streamlit as st
from streamlit_chat import message

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

    # user_input = st.text_input("Enter your message:")
    # if st.button("Send"):
    #     if user_input:
    #         response = send_message(user_input)
    #         st.text("Server Response:")
    #         st.text(response)

    response_container = st.container()
    textcontainer = st.container()

    details = ""

    if "responses" not in st.session_state:
        st.session_state["responses"] = ["I'm here to assist you!"]

    if "requests" not in st.session_state:
        st.session_state["requests"] = []

    if "buffer_memory" not in st.session_state:
        st.session_state.buffer_memory = ""

    with textcontainer:
        query = st.text_input("You: ", key="input", placeholder="start chat")
        submit = st.button("Send")
        if submit:
            # res = qa({"question": query})
            # response = print_answer_metadata(res)
            response = send_message(query)
            # details = print_page_content(res)
            st.session_state.requests.append(query)
            st.session_state.responses.append(response)

    with response_container:
        if st.session_state["responses"]:
            for i in range(len(st.session_state["responses"])):
                message(
                    st.session_state["responses"][i],
                    key=str(i),
                    avatar_style="no-avatar",
                    # logo=logo(),
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
