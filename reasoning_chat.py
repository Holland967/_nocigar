import streamlit as st
# from dotenv import load_dotenv
import os

from chat import Chat

# load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL")
c = Chat(api_key, base_url)

def reasoningChat():
    if "r_msg" not in st.session_state:
        st.session_state.r_msg = []
    if "reasoning_msg" not in st.session_state:
        st.session_state.reasoning_msg = []

    with st.sidebar:
        clear_btn = st.button("Clear Chat", key="r_clear_btn", type="primary", use_container_width=True)

    for reason, msg in zip(st.session_state.reasoning_msg, st.session_state.r_msg):
        with st.expander("Thinking"):
            st.markdown(reason)
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if query := st.chat_input("Say something...", key="r_query"):
        st.session_state.r_msg.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        messages = [] + st.session_state.r_msg
        response = c.reason_completion(messages)
        with st.expander("Thinking", expanded=True):
            reasoning = st.write_stream(chunk.choices[0].delta.reasoning_content for chunk in response if chunk.choices[0].delta.reasoning_content is not None)
        with st.chat_message("assistant"):
            message = st.write_stream(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        st.session_state.reasoning_msg.append(reasoning)
        st.session_state.r_msg.append({"role": "assistant", "content": message})
        st.rerun()

    if clear_btn:
        st.session_state.r_msg = []
        st.session_state.r_cache = []
        st.rerun()

if __name__ == "__main__":
    reasoningChat()
