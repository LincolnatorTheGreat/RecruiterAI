import datetime
import re
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader


import pypandoc

try:
    pypandoc.get_pandoc_path()
except OSError:
    print("Pandoc not found. Please install pandoc to use .docx and .odt files.")


def read_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        elif ext in ['.docx', '.odt']:
            text = pypandoc.convert_file(file_path, 'plain')
            # Cleanup: replace carriage returns with newlines and remove other non-printable ASCII characters
            text = text.replace('\r', '\n') # Replace ^M with newline
            # Remove other non-printable ASCII characters (control characters)
            # Keep printable ASCII characters (32-126) and common whitespace (tab, newline)
            text = re.sub(r'[^\x20-\x7E\t\n]', '', text)
            return text.strip()
        elif ext in ['.md', '.txt', '.rtf']:  # Basic text, RTF as text (may have formatting junk)
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            print(f"Unsupported file type: {file_path}")
            return None
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def get_latest_file(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f != '.gitkeep']
    if not files:
        return None
    return os.path.join(folder, max(files, key=lambda f: os.path.getmtime(os.path.join(folder, f))))

def move_to_old(file_path, old_folder):
    if os.path.exists(file_path):
        base_name = os.path.basename(file_path)
        destination_path = os.path.join(old_folder, base_name)

        # If a file with the same name already exists in the old_folder,
        # append a timestamp to the filename to make it unique.
        if os.path.exists(destination_path):
            name, ext = os.path.splitext(base_name)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_base_name = f"{name}_{timestamp}{ext}"
            destination_path = os.path.join(old_folder, new_base_name)

        shutil.move(file_path, destination_path)

def convert_to_md(file_path, output_folder):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Generate a unique name for the .md output file
    md_name = f"{base_name}.md"
    counter = 1
    while os.path.exists(os.path.join(output_folder, md_name)):
        md_name = f"{base_name}_{counter}.md"
        counter += 1
        
    md_path = os.path.join(output_folder, md_name)
    
    text = read_file(file_path)
    if text is None:
        return None
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return md_path

def archive_all_files_in_folder(folder_path):
    old_folder = os.path.join(folder_path, "old_files")
    os.makedirs(old_folder, exist_ok=True)
    
    for f in os.listdir(folder_path):
        if f == '.gitkeep':
            continue
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path): # Only process files, not subdirectories
            move_to_old(file_path, old_folder)

def process_uploaded_file(uploaded_file, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    old_folder = os.path.join(target_folder, "old_files")
    os.makedirs(old_folder, exist_ok=True)
    
    temp_path = os.path.join(target_folder, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    convert_to_md(temp_path, target_folder)
    move_to_old(temp_path, old_folder)

def process_and_display_files(folder_path, file_type):
    os.makedirs(folder_path, exist_ok=True)
    old_folder = os.path.join(folder_path, "old_files")
    os.makedirs(old_folder, exist_ok=True)

    # Get all .md files in the folder
    md_files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.md') and f != '.gitkeep'],
                      key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=True)
    return md_files
def archive_old_letters():
    OUTPUT_FOLDER = "outputs"
    OLD_OUTPUTS = os.path.join(OUTPUT_FOLDER, "old_files")
    os.makedirs(OLD_OUTPUTS, exist_ok=True)
    old_letters = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith('.txt') and os.path.isfile(os.path.join(OUTPUT_FOLDER, f)) and f != '.gitkeep']
    for old in old_letters:
        shutil.move(os.path.join(OUTPUT_FOLDER, old), os.path.join(OLD_OUTPUTS, old))

def get_tech_library_content():
    tech_folder = os.path.join("static_assets", "tech_library")
    files = [f for f in os.listdir(tech_folder) if f.endswith('.md') and os.path.isfile(os.path.join(tech_folder, f)) and f != '.gitkeep']
    content = ""
    for f in files:
        content += read_.read_file(os.path.join(tech_folder, f)) + "\n\n"
    return content.strip()
