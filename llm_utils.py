import os
import google.generativeai as genai
from openai import OpenAI

def get_gemini_models():
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY_RECAI'), transport='rest')
        return [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    except Exception as e:
        print(f"Error getting Gemini models: {e}")
        return []

def get_openai_models():
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        return [model.id for model in client.models.list()]
    except Exception as e:
        print(f"Error getting OpenAI models: {e}")
        return []
