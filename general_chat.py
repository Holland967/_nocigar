import streamlit as st
# from dotenv import load_dotenv
import os

from chat import Chat

# load_dotenv()
siliconflow_api_key = os.getenv("SILICONFLOW_API_KEY")
siliconflow_base_url = os.getenv("SILICONFLOW_BASE_URL")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL")

model_list = [
    "Qwen/Qwen2.5-72B-Instruct",
    "deepseek-chat",
    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-405B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct-128K"
]

default_system_prompt = """
You are a helpful assistant.
"""

def generalChat():
    if "g_msg" not in st.session_state:
        st.session_state.g_msg = []
    if "g_cache" not in st.session_state:
        st.session_state.g_cache = []
    if "g_retry" not in st.session_state:
        st.session_state.g_retry = False

    with st.sidebar:
        clear_btn = st.button("Clear Chat", key="g_clear_btn", type="primary", use_container_width=True)
        undo_btn = st.button("Undo", key="g_undo_btn", use_container_width=True)
        retry_btn = st.button("Retry", key="g_retry_btn", use_container_width=True)
        model = st.selectbox("Model", model_list, index=0, key="g_model")
        system_prompt = st.text_area("System Prompt", default_system_prompt, key="g_sys")
        temperature = st.slider("Temperature", 0.00, 2.00, 0.70, 0.01, key="g_temp")
        top_p = st.slider("Top P", 0.01, 1.00, 0.70, 0.01, key="g_topp")
        frequency_penalty = st.slider("Frequency Penalty", -2.00, 2.00, 0.00, 0.01, key="g_freq")
        presence_penalty = st.slider("Presence Penalty", -2.00, 2.00, 0.00, 0.01, key="g_pres")

    if model == "deepseek-chat":
        c = Chat(api_key=deepseek_api_key, base_url=deepseek_base_url)
    else:
        c = Chat(api_key=siliconflow_api_key, base_url=siliconflow_base_url)

    for i in st.session_state.g_cache:
        with st.chat_message(i["role"]):
            st.markdown(i["content"])

    if query := st.chat_input("Say something...", key="g_query"):
        st.session_state.g_msg.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.g_msg
        with st.chat_message("assistant"):
            response = c.chat_completion(messages, model, temperature, top_p, frequency_penalty, presence_penalty)
            result = st.write_stream(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        st.session_state.g_msg.append({"role": "assistant", "content": result})
        st.session_state.g_cache = st.session_state.g_msg
        st.rerun()

    if clear_btn:
        st.session_state.g_msg = []
        st.session_state.g_cache = []
        st.rerun()

    if undo_btn:
        del st.session_state.g_msg[-1]
        del st.session_state.g_cache[-1]
        st.rerun()

    if retry_btn:
        st.session_state.g_msg.pop()
        st.session_state.g_cache = []
        st.session_state.g_retry = True
        st.rerun()
    if st.session_state.g_retry:
        for i in st.session_state.g_msg:
            with st.chat_message(i["role"]):
                st.markdown(i["content"])
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.g_msg
        with st.chat_message("assistant"):
            response = c.chat_completion(messages, model, temperature, top_p, frequency_penalty, presence_penalty)
            result = st.write_stream(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        st.session_state.g_msg.append({"role": "assistant", "content": result})
        st.session_state.g_cache = st.session_state.g_msg
        st.session_state.g_retry = False
        st.rerun()

if __name__ == "__main__":
    generalChat()
