import streamlit as st
# from dotenv import load_dotenv
import os

from general_chat import generalChat
from reasoning_chat import reasoningChat
from image_generation import imageGeneration
from speach_transcription import speachTranscription
from text_speaking import textSpeaking

# load_dotenv()
pass_word = os.getenv("PASSWORD")

if "login_status" not in st.session_state:
    st.session_state.login_status = False

def login():
    if not st.session_state.login_status:
        password = st.text_input("Password", "", key="password", type="password")
        login_btn = st.button("Login", key="login_btn", type="primary")
        if login_btn and password:
            if password == pass_word:
                st.session_state.login_status = True
                st.rerun()
            else:
                st.error("Wrong password")
    else:
        main()

def main():
    with st.sidebar:
        function_list = [
            "General Chat",
            "Reasoning Chat",
            "Image Generation",
            "Speech Transcription",
            "Text Speaking"
        ]
        functions = st.selectbox("Select Function", function_list, index=0, key="functions")
    if functions == "General Chat":
        generalChat()
    elif functions == "Reasoning Chat":
        reasoningChat()
    elif functions == "Image Generation":
        imageGeneration()
    elif functions == "Speech Transcription":
        speachTranscription()
    elif functions == "Text Speaking":
        textSpeaking()
    
    log_out = st.sidebar.button("Logout", key="logout")
    if log_out:
        st.session_state.login_status = False
        st.rerun()

if __name__ == "__main__":
    login()
