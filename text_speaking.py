import streamlit as st
from openai import OpenAI
from pathlib import Path
# from dotenv import load_dotenv
import os

# load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")
base_url = os.getenv("SILICONFLOW_BASE_URL")

speech_file_path = Path(__file__).parent / "siliconcloud-generated-speech.mp3"

model_list = [
    "RVC-Boss/GPT-SoVITS",
    "FunAudioLLM/CosyVoice2-0.5B"
]

url = "https://api.siliconflow.cn/v1/audio/speech"

sovits_voice_list = [
    "RVC-Boss/GPT-SoVITS:alex",
    "RVC-Boss/GPT-SoVITS:anna",
    "RVC-Boss/GPT-SoVITS:bella",
    "RVC-Boss/GPT-SoVITS:benjamin",
    "RVC-Boss/GPT-SoVITS:charles",
    "RVC-Boss/GPT-SoVITS:claire",
    "RVC-Boss/GPT-SoVITS:david",
    "RVC-Boss/GPT-SoVITS:diana"
]

cosy_voice_list = [
    "FunAudioLLM/CosyVoice2-0.5B:alex",
    "FunAudioLLM/CosyVoice2-0.5B:anna",
    "FunAudioLLM/CosyVoice2-0.5B:bella",
    "FunAudioLLM/CosyVoice2-0.5B:benjamin",
    "FunAudioLLM/CosyVoice2-0.5B:charles",
    "FunAudioLLM/CosyVoice2-0.5B:claire",
    "FunAudioLLM/CosyVoice2-0.5B:david",
    "FunAudioLLM/CosyVoice2-0.5B:diana"
]

def textSpeaking():
    with st.sidebar:
        model = st.selectbox("Model", model_list, index=0, key="text_to_speach_model")
        speed = st.slider("Speed", 0.25, 4.00, 1.00, 0.01, key="text_to_speach_speed")
        if model == "RVC-Boss/GPT-SoVITS":
            voice = st.selectbox("Voice", sovits_voice_list, index=0, key="sovits_voice")
        elif model == "FunAudioLLM/CosyVoice2-0.5B":
            voice = st.selectbox("Voice", cosy_voice_list, index=0, key="cosy_voice")

    prompt = st.text_area("Prompt", "", key="text_prompt")
    generate = st.button("Generate", key="text_to_speach", type="primary")

    if generate and prompt:
        client = OpenAI(api_key=api_key, base_url=base_url)

        with st.spinner("Generating..."):
            with client.audio.speech.with_streaming_response.create(
                model=model,
                voice=voice,
                input=prompt,
                speed=speed,
                response_format="mp3"
            ) as response:
                response.stream_to_file(speech_file_path)
        
        st.audio(str(speech_file_path), format="audio/mp3")
    elif generate and not prompt:
        st.warning("Please enter a prompt.")

if __name__ == "__main__":
    textSpeaking()
