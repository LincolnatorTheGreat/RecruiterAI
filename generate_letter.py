import datetime
import os
import google.generativeai as genai
import sys
import time
import shutil
from file_utils import read_file, get_latest_file, move_to_old, convert_to_md, archive_old_letters, get_tech_library_content

# Gemini config
API_KEY = os.getenv('GEMINI_API_KEY_RECAI')
if not API_KEY:
    print("Set GEMINI_API_KEY_RECAI env var or hardcode it!")
    sys.exit(1)
genai.configure(api_key=API_KEY, transport='rest')

MODEL_GENERATE = 'gemini-2.5-flash'
model_generate = genai.GenerativeModel(MODEL_GENERATE)

# Folders
INPUT_FOLDER = "candidate_inputs"
STATIC_FOLDER = "static_assets"
OUTPUT_FOLDER = "outputs"
OLD_OUTPUTS = os.path.join(OUTPUT_FOLDER, "old_files")
os.makedirs(OLD_OUTPUTS, exist_ok=True)

def call_gemini(prompt, call_name="AI call", model_name="unknown"):
    start_time = time.time()
    start_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Capture start datetime
    try:
        response = model_generate.generate_content(prompt)
        duration = time.time() - start_time
        log_message = f"[{start_datetime}] {call_name} ({model_name}) took {duration:.2f} seconds"
        print(log_message)
        
        # Ensure the logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Append the log message to the logs.txt file
        with open("./logs/logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_message + "\n")
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        sys.exit(1)

def generate_letter(resume_path):

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
    
    template = read_file(get_latest_file(os.path.join(STATIC_FOLDER, "message_template")))
    if template.startswith("Error reading"):
        return template
    system_prompt = read_file(get_latest_file(os.path.join(STATIC_FOLDER, "system_prompt")))
    if system_prompt.startswith("Error reading"):
        return system_prompt
    tech_library = get_tech_library_content()
    if tech_library.startswith("Error reading"):
        return tech_library

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
        generated_letter = call_gemini(full_prompt, "Generation AI call", MODEL_GENERATE)
    except Exception as e:
        return f"An error occurred during letter generation: {e}"
    
    return generated_letter

