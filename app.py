import streamlit as st
import os
import shutil
import datetime
from generate_letter import generate_letter
from file_utils import convert_to_md, move_to_old, get_latest_file, archive_old_letters, process_and_display_files, process_uploaded_file, archive_all_files_in_folder

def load_letters_into_session_state():
    st.session_state.generated_letters = [] # Clear existing letters
    OUTPUT_FOLDER = "outputs"
    OLD_OUTPUTS = os.path.join(OUTPUT_FOLDER, "old_files")
    
    if os.path.exists(OUTPUT_FOLDER):
        # Get all .txt files in the outputs folder, excluding the old_files subfolder
        all_output_files = []
        for f in os.listdir(OUTPUT_FOLDER):
            file_path = os.path.join(OUTPUT_FOLDER, f)
            if os.path.isfile(file_path) and file_path.endswith('.txt') and not file_path.startswith(OLD_OUTPUTS + os.sep):
                all_output_files.append(file_path)

        # Sort the current letters by modification time, newest first
        all_output_files.sort(key=os.path.getmtime, reverse=True)

        for file_path in all_output_files:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    letter_content = f.read()
                st.session_state.generated_letters.append((filename, letter_content))
            except Exception as e:
                st.warning(f"Could not read existing letter {filename}: {e}")
        


# Page config
st.set_page_config(page_title="Recruiter Letter Generator", layout="wide")

st.title("🤖 Personalized Recruiter Letter Generator")
st.markdown("Upload JD and Resume, hit Generate—get your letter in seconds!")

# Session state
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'generated_letters' not in st.session_state:
    st.session_state.generated_letters = []
if 'processing_resume_name' not in st.session_state:
    st.session_state.processing_resume_name = None
if 'processed_upload_ids' not in st.session_state:
    st.session_state.processed_upload_ids = []


# JD Section
st.subheader("📋 Job Description")
jd_folder = "candidate_inputs/jd"
current_jd_files = process_and_display_files(jd_folder, "jd")

jd_file = st.file_uploader("Upload JD (PDF/TXT/DOCX/ODT)", type=['pdf', 'txt', 'docx', 'odt'], key="jd", disabled=st.session_state.generating)

if jd_file:
    file_identifier = (jd_file.name, jd_file.size)
    if file_identifier not in st.session_state.processed_upload_ids:
        jd_folder = "candidate_inputs/jd"
        
        # Archive all existing files in the jd_folder before processing the new one
        archive_all_files_in_folder(jd_folder)

        process_uploaded_file(jd_file, jd_folder)
        st.session_state.processed_upload_ids.append(file_identifier)
        st.success("JD uploaded and converted!")
        st.rerun()

if current_jd_files:
    active_jd_path = os.path.join(jd_folder, current_jd_files[0])
    
    col_jd_name, col_jd_remove = st.columns([0.8, 0.2])
    with col_jd_name:
        st.markdown(f"**Current JD:** {current_jd_files[0]}")
    with col_jd_remove:
        if st.button("❌ Remove JD", key="remove_current_jd", disabled=st.session_state.generating):
            archive_all_files_in_folder(jd_folder) # Archive all JDs, effectively removing the current one
            st.rerun()
    
    # Display first 25 lines of active JD
    try:
        with open(active_jd_path, 'r', encoding='utf-8') as f:
            jd_preview_lines = f.readlines()[:25]
        st.text_area("JD Preview (First 25 Lines)", "".join(jd_preview_lines), height=150, key="jd_preview", disabled=True)
    except UnicodeDecodeError:
        st.error(f"Could not display preview for '{current_jd_files[0]}'. The file might be corrupted or have an unsupported encoding.")
    except Exception as e:
        st.error(f"An error occurred while reading '{current_jd_files[0]}': {e}")

def process_uploaded_file(uploaded_file, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    old_folder = os.path.join(target_folder, "old_files")
    os.makedirs(old_folder, exist_ok=True)
    
    # Generate a unique name for the original uploaded file in the old_files folder
    original_base_name = uploaded_file.name
    original_name_without_ext, original_ext = os.path.splitext(original_base_name)
    
    unique_original_file_name = original_base_name
    counter = 1
    while os.path.exists(os.path.join(old_folder, unique_original_file_name)):
        unique_original_file_name = f"{original_name_without_ext}_{counter}{original_ext}"
        counter += 1
        
    original_file_in_old_path = os.path.join(old_folder, unique_original_file_name)
    
    # Save the uploaded file directly to the old_files folder with a unique name
    with open(original_file_in_old_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if original_ext.lower() == '.md':
        # If it's already a markdown file, copy it from old_files to target_folder
        # The copy operation itself needs to handle unique naming in target_folder
        target_md_name = f"{original_name_without_ext}.md"
        md_counter = 1
        while os.path.exists(os.path.join(target_folder, target_md_name)):
            target_md_name = f"{original_name_without_ext}_{md_counter}.md"
            md_counter += 1
        shutil.copy(original_file_in_old_path, os.path.join(target_folder, target_md_name))
    else:
        # For non-md files, convert to md from the file in old_files
        # and place the resulting .md file in the target_folder.
        # convert_to_md needs to handle unique naming for its output.
        convert_to_md(original_file_in_old_path, target_folder)


# Resume Section
st.subheader("👤 Candidate Resumes")

# Resume Upload
resume_folder = "candidate_inputs/resume"
resume_files = st.file_uploader("Upload Resume (PDF/TXT/DOCX/ODT/MD)", type=['pdf', 'txt', 'docx', 'odt', 'md'], key="resume", disabled=st.session_state.generating, accept_multiple_files=True)

if resume_files:
    newly_processed = False
    for resume_file in resume_files:
        # Create a unique identifier for the uploaded file using its name and size
        file_identifier = (resume_file.name, resume_file.size)
        
        if file_identifier not in st.session_state.processed_upload_ids:
            process_uploaded_file(resume_file, resume_folder)
            st.session_state.processed_upload_ids.append(file_identifier)
            newly_processed = True
    
    if newly_processed:
        st.success("Resumes uploaded and converted!")
        st.rerun()

# Display Active Resumes
st.markdown("---")
st.markdown("**Used resumes ready to be regenerated:**")
active_folder = os.path.join(resume_folder, "active_resumes")
active_resumes = sorted([f for f in os.listdir(active_folder) if os.path.isfile(os.path.join(active_folder, f))],
                        key=lambda f: os.path.getmtime(os.path.join(active_folder, f)))  # Oldest first

if active_resumes:
    for f in active_resumes:
        col_name, col_button = st.columns([0.8, 0.2])
        with col_name:
            color = "green" if st.session_state.get("processing_resume_name") == f else "red"
            st.markdown(f"<span style='color:{color}'>{f} (Active)</span>", unsafe_allow_html=True)
        with col_button:
            if st.button("❌ Remove", key=f"remove_active_{f}", disabled=st.session_state.generating):
                shutil.move(os.path.join(active_folder, f), os.path.join(resume_folder, "old_files", f))
                st.rerun()
else:
    st.info("No active resumes for generation.")

# Display Regular Resumes
st.markdown("---")
st.markdown("**Available Resumes:**")
regular_resumes = sorted([f for f in os.listdir(resume_folder) if os.path.isfile(os.path.join(resume_folder, f)) and f.endswith('.md')],
                         key=lambda f: os.path.getmtime(os.path.join(resume_folder, f)), reverse=True)  # Newest first

if regular_resumes:
    for f in regular_resumes:
        col_name, col_button = st.columns([0.8, 0.2])
        with col_name:
            st.markdown(f"{f}")
        with col_button:
            if st.button("❌ Remove", key=f"remove_regular_{f}", disabled=st.session_state.generating):
                shutil.move(os.path.join(resume_folder, f), os.path.join(resume_folder, "old_files", f))
                st.rerun()
else:
    st.info("No available resumes.")

# Resume Control Buttons
st.markdown("---")
col_remove_used, col_clear_all = st.columns(2)

with col_remove_used:
    if st.button("Remove Used Resumes", disabled=len(active_resumes) == 0 or st.session_state.generating):
        for f in active_resumes:
            shutil.move(os.path.join(active_folder, f), os.path.join(resume_folder, "old_files", f))
        st.rerun()

with col_clear_all:
    if st.button("Clear All Resumes", disabled=st.session_state.generating):
        for f in regular_resumes:
            shutil.move(os.path.join(resume_folder, f), os.path.join(resume_folder, "old_files", f))
        for f in active_resumes:
            shutil.move(os.path.join(active_folder, f), os.path.join(resume_folder, "old_files", f))
        st.rerun()

st.markdown("---") # Separator for the new button
if st.button("Clear Generated Letters", disabled=st.session_state.generating):
    archive_old_letters()
    load_letters_into_session_state() # Update session state to reflect cleared letters
    st.rerun()

# Generate
generate_label = "Generating..." if st.session_state.generating else "✨ Generate Letters (Up to 5)"
if st.button(generate_label, disabled=st.session_state.generating):
    st.session_state.generating = True
    st.rerun()

if st.session_state.generating:
    with st.spinner("Generating..."):
        resume_folder = "candidate_inputs/resume"
        active_folder = os.path.join(resume_folder, "active_resumes")
        os.makedirs(active_folder, exist_ok=True)
        
        active_resumes = [f for f in os.listdir(active_folder) if os.path.isfile(os.path.join(active_folder, f))]
        while len(active_resumes) < 5:
            regular_resumes = [f for f in os.listdir(resume_folder) if os.path.isfile(os.path.join(resume_folder, f)) and f.endswith('.md')]
            if not regular_resumes:
                break
            # Most recent
            latest_regular = max(regular_resumes, key=lambda f: os.path.getmtime(os.path.join(resume_folder, f)))
            shutil.move(os.path.join(resume_folder, latest_regular), os.path.join(active_folder, latest_regular))
            active_resumes.append(latest_regular)
        
        archive_old_letters()
        load_letters_into_session_state() # Clear old letters from display (will be reflected on final rerun)
        
        for resume in active_resumes:
            st.session_state.processing_resume_name = resume # Set processing status (will be reflected on final rerun)

            letter = generate_letter(os.path.join(active_folder, resume))
            if letter and not letter.startswith("An error occurred"):
                # Extract candidate name from resume filename
                name = os.path.splitext(os.path.basename(resume))[0]
                base_name = name
                dup_count = 1
                
                generated_base_names = [fn.split('=')[0] for fn, _ in st.session_state.generated_letters]

                while base_name in generated_base_names:
                    base_name = f"{name}_{dup_count}"
                    dup_count += 1

                now = datetime.datetime.now()
                timestamp = now.strftime("%m%d%Y%H%M")
                filename = f"{base_name}={timestamp}.txt"
                
                output_path = os.path.join("outputs", filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(letter)
                
                load_letters_into_session_state() # Update displayed letters with the new one (will be reflected on final rerun)
            elif letter:
                st.error(letter)
            
            st.session_state.processing_resume_name = None # Reset processing status (will be reflected on final rerun)

        st.session_state.generating = False
        st.rerun() # Final rerun to update all UI elements

# Generated letters
st.markdown("--- ")
st.subheader("Generated Letters")
st.info("**Pro-Tip:** To copy a letter, click inside the desired letter's text box and press `Ctrl+A` (or `Cmd+A` on Mac) to select all the text in that box, then `Ctrl+C` (or `Cmd+C`) to copy.")
load_letters_into_session_state()

# Display letters from session state
for filename, letter in st.session_state.generated_letters:
    st.subheader(filename)
    st.text_area(f"Letter for {filename}", letter, height=300, key=f"letter_content_{filename}")

# Footer
st.markdown("---")
st.caption("Built with Streamlit & Gemini API | Local only")
