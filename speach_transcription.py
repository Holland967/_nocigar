from openai import OpenAI
import streamlit as st
# from dotenv import load_dotenv
import os

# load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")
base_url = os.getenv("SILICONFLOW_BASE_URL")
client = OpenAI(api_key=api_key, base_url=base_url)

def speachTranscription():
    audio = st.file_uploader("Upload", type=["mp3", "wav"], key="upload_audio")
    generate = st.button("Generate", key="uploading_audio", type="primary")
    if audio is not None:
        st.audio(audio)
    if generate and audio is not None:
        with st.spinner("Generating..."):
            response = client.audio.transcriptions.create(
                model="FunAudioLLM/SenseVoiceSmall",
                file=audio
            )
            st.markdown(response.text)

if __name__ == "__main__":
    speachTranscription()
