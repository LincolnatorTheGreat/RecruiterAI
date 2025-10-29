import streamlit as st
import os
import subprocess
from dotenv import load_dotenv, set_key
from llm_utils import get_gemini_models, get_openai_models

load_dotenv()

st.set_page_config(layout="wide")

st.title("Model Configuration")

def get_ollama_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        # Skip the header line and parse the model names
        models = [line.split()[0] for line in lines[1:]]
        print(f"Ollama models found: {models}")
        return models
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error getting Ollama models: {e}")
        return ["granite4:micro-h", "llama2"] # Fallback models

# Initialize session state from environment variables if not already set
if "RECAI_MODEL_API" not in st.session_state:
    st.session_state.RECAI_MODEL_API = os.getenv("RECAI_MODEL_API", "gemini")
if "RECAI_MODEL_ID" not in st.session_state:
    st.session_state.RECAI_MODEL_ID = os.getenv("RECAI_MODEL_ID", "gemini-2.5-flash")

# Create the UI elements
selected_api = st.selectbox("Select API", ["gemini", "openai", "ollama", "llama_local"], index=["gemini", "openai", "ollama", "llama_local"].index(st.session_state.RECAI_MODEL_API))

# Update the available models based on the selected API
if selected_api == "gemini":
    available_models = get_gemini_models()
elif selected_api == "openai":
    available_models = get_openai_models()
elif selected_api == "ollama":
    available_models = get_ollama_models()
else:
    available_models = []

selected_model = st.selectbox("Select Model", available_models, index=available_models.index(st.session_state.RECAI_MODEL_ID) if st.session_state.RECAI_MODEL_ID in available_models else 0)

if st.button("Save Configuration"):
    # Update the .env file
    set_key(".env", "RECAI_MODEL_API", selected_api)
    set_key(".env", "RECAI_MODEL_ID", selected_model)

    # Update the session state
    st.session_state.RECAI_MODEL_API = selected_api
    st.session_state.RECAI_MODEL_ID = selected_model
    
    st.success(f"Configuration saved. API: {selected_api}, Model: {selected_model}")
    # Force a rerun to reflect the new environment variables
    st.rerun()

st.write(f"Current API: {st.session_state.RECAI_MODEL_API}")
st.write(f"Current Model: {st.session_state.RECAI_MODEL_ID}")
