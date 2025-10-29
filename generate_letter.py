import datetime
import os
import sys
import time
import shutil
import google.generativeai as genai
from openai import OpenAI
from file_utils import read_file, get_latest_file, get_tech_library_content

# Folders
INPUT_FOLDER = "candidate_inputs"
STATIC_FOLDER = "static_assets"
OUTPUT_FOLDER = "outputs"
OLD_OUTPUTS = os.path.join(OUTPUT_FOLDER, "old_files")
os.makedirs(OLD_OUTPUTS, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def get_llm_client(recai_model_api, recai_model_id):
    if recai_model_api == 'gemini':
        api_key = os.getenv('GEMINI_API_KEY_RECAI')
        if not api_key:
            raise ValueError("GEMINI_API_KEY_RECAI environment variable not set.")
        genai.configure(api_key=api_key, transport='rest')
        model_id = recai_model_id or 'gemini-2.5-flash'
        return genai.GenerativeModel(model_id), model_id
    elif recai_model_api == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        model_id = recai_model_id or 'gpt-4o'
        return OpenAI(api_key=api_key), model_id
    elif recai_model_api == 'llama_local':
        model_id = recai_model_id or 'granite4:micro-h'
        return OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed"), model_id
    elif recai_model_api == 'ollama':
        model_id = recai_model_id or 'granite4:micro-h'
        return OpenAI(base_url="http://localhost:11434/v1", api_key="not-needed"), model_id
    else:
        raise ValueError(f"Unsupported API: {recai_model_api}")
def log_generation(call_name, model_name, duration, input_tokens, output_tokens):
    start_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{start_datetime}] {call_name} ({model_name}) took {duration:.2f} seconds, Input Tokens: {input_tokens}, Output Tokens: {output_tokens}"
    print(log_message)
    with open("./logs/logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")

def generate_with_gemini(client, prompt, model_id):
    start_time = time.time()
    response = client.generate_content(prompt)
    duration = time.time() - start_time
    
    input_tokens = client.count_tokens(prompt).total_tokens
    output_tokens = client.count_tokens(response.text).total_tokens
    
    log_generation("Gemini Call", model_id, duration, input_tokens, output_tokens)
    return response.text.strip()

def generate_with_openai(client, prompt, model_id):
    start_time = time.time()
    try:
        print(f"Sending request to OpenAI/Ollama with model: {model_id}")
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"Received response from OpenAI/Ollama: {response}")
        duration = time.time() - start_time
        
        # Token usage from response
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        
        log_generation("OpenAI Call", model_id, duration, input_tokens, output_tokens)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in generate_with_openai: {e}")
        return f"An error occurred during letter generation: {e}"

def generate_letter(resume_path, recai_model_api, recai_model_id):
    try:
        client, model_id = get_llm_client(recai_model_api, recai_model_id)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    jd_folder = os.path.join(INPUT_FOLDER, "jd")
    jd_path = get_latest_file(jd_folder)
    if not jd_path:
        print("Error: No JD found")
        return None

    jd_text = read_file(jd_path)
    if jd_text.startswith("Error reading"):
        return jd_text
    resume_text = read_file(resume_path)
    if resume_text.startswith("Error reading"):
        return resume_text
    
    template_path = get_latest_file(os.path.join(STATIC_FOLDER, "message_template"))
    template = read_file(template_path) if template_path else ""
    
    system_prompt_path = get_latest_file(os.path.join(STATIC_FOLDER, "system_prompt"))
    system_prompt = read_file(system_prompt_path) if system_prompt_path else ""
    
    tech_library = get_tech_library_content()

    full_prompt = f"""
    {system_prompt}

    Job Description:
    {jd_text}

    Candidate Resume:
    {resume_text}

    Company Tech Library:
    {tech_library}

    Message Template to personalize:
    {template}
    
    Generate the final personalized letter now.
    """
    
    try:
        if recai_model_api == 'gemini':
            return generate_with_gemini(client, full_prompt, model_id)
        elif recai_model_api in ['openai', 'llama_local', 'ollama']:
            return generate_with_openai(client, full_prompt, model_id)
    except Exception as e:
        print(f"An error occurred during letter generation: {e}")
        return f"An error occurred during letter generation: {e}"
    
    return None

