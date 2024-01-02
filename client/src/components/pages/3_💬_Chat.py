from openai import OpenAI
import streamlit as st
import requests

st.set_page_config(page_title="Chat", page_icon="💬")
st.image("./images/bot.PNG", width=500)
st.sidebar.header("Chat")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
avatar = {"user": "./images/human.png", "assistant":"./images/logo.PNG"}

uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files = True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
#    st.write(bytes_data)

ai_models = ("gpt-3.5-turbo","gpt-4","gpt-4-32k")
model_choice = st.selectbox(
    'Please select AI Model',
    ai_models)
#####st.write(f"Your choice: {model_choice}")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_choice

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = avatar[message["role"]]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask question here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar = avatar["user"]):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar = avatar["assistant"]):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})