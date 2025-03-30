import streamlit as st
from google import genai
import time


import re
# Title and subtitle
st.set_page_config(page_title="My Chatbot", layout="centered")
st.title("Hi! I'm your assistant")
st.caption("Ask me anything and I'll try my best to help!")






def gen_response(chat, prompt):
    response = chat.send_message(prompt).text.strip()
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Split into text and code blocks using regex
    parts = re.split(r"(```.*?```)", response, flags=re.DOTALL)

    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            # Remove the triple backticks and optional language tag
            code_content = part.strip("```").lstrip("\n")
            st.markdown(code_content)
        else:
            # Typing effect for text sections
            output = ""
            md_box = st.empty()
            for char in part:
                output += char
                md_box.markdown(output)
                time.sleep(0.001)
# Store chat history
def main():
    api_key = st.secrets["api_key"]
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.0-flash")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message('user'):
            st.markdown(user_input)
        # Get response from bot



        # Show assistant response
        with st.chat_message("assistant"):
            gen_response(chat,user_input)
main()