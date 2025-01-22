import streamlit as st
import requests
# from dotenv import load_dotenv
import os

# load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")

url = "https://api.siliconflow.cn/v1/images/generations"

model_list = [
    "black-forest-labs/FLUX.1-dev",
    "stabilityai/stable-diffusion-3-5-large"
]

def imageGeneration():
    with st.sidebar:
        model = st.selectbox("Model", model_list, index=0, key="image_model")

    if model == "black-forest-labs/FLUX.1-dev":
        img_size_list = [
            "1024x1024",
            "960x1280",
            "768x1024",
            "720x1440",
            "720x1280",
            "others"
        ]

        image_size = st.sidebar.selectbox("Image Size", img_size_list, index=0, key="flux_image_size")
        if image_size == "others":
            image_size = st.sidebar.text_input("Image Size", "1280x960", key="flux_image_size_others", label_visibility="collapsed")
        num_inference_steps = st.sidebar.slider("Step", 1, 30, 30, key="flux_num_inference_steps")
        prompt_enhancement = st.sidebar.toggle("Prompt Enhancement", key="flux_prompt_enhancement")

        prompt = st.text_area("Prompt", "", key="flux_prompt")
        generate = st.button("Generate", key="flux_generate", type="primary")

        if generate and prompt:
            payload = {
                "model": model,
                "prompt": prompt,
                "image_size": image_size,
                "num_inference_steps": num_inference_steps,
                "prompt_enhancement": prompt_enhancement
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            with st.spinner("Generating..."):
                response = requests.request("POST", url, json=payload, headers=headers)
            response_object = response.json()
            image_data = response_object["images"]
            image_url = image_data[0]["url"]
            if image_url:
                st.image(image_url, output_format="PNG")
        elif generate and not prompt:
            st.warning("Please enter a prompt.")
    elif model == "stabilityai/stable-diffusion-3-5-large":
        image_size = [
            "1024x1024",
            "512x1024",
            "768x512",
            "768x1024",
            "1024x576",
            "576x1024"
        ]

        image_size = st.sidebar.selectbox("Image Size", image_size, index=0, key="sd_image_size")
        num_inference_steps = st.sidebar.slider("Step", 1, 50, 35, key="sd_num_inference_steps")
        guidance_scale = st.sidebar.slider("Guidance Scale", 1.0, 20.0, 7.5, key="sd_guidance_scale")
        prompt_enhancement = st.sidebar.toggle("Prompt Enhancement", key="sd_prompt_enhancement")

        prompt = st.text_area("Prompt", "", key="sd_prompt")
        negative_prompt = st.text_area("Negative Prompt", "", key="sd_negative_prompt")
        generate = st.button("Generate", key="sd_generate", type="primary")

        if generate and prompt:
            payload = {
                "model": model,
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "image_size": image_size,
                "batch_size": 1,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "prompt_enhancement": prompt_enhancement
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            with st.spinner("Generating..."):
                response = requests.request("POST", url, json=payload, headers=headers)
            response_object = response.json()
            image_data = response_object["images"]
            image_url = image_data[0]["url"]
            if image_url:
                st.image(image_url, output_format="PNG")
        elif generate and not prompt:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    imageGeneration()
