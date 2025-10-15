import os
import streamlit as st
from file_utils import get_latest_file, move_to_old, convert_to_md, process_uploaded_file, process_and_display_files, archive_all_files_in_folder

if 'processed_upload_ids' not in st.session_state:
    st.session_state.processed_upload_ids = []

# Config page title
st.title("Config Page")

# Link back to home
st.page_link("app.py", label="Back to Home")

# Message Template
st.subheader("Message Template")
template_folder = "static_assets/message_template"
current_template_files = process_and_display_files(template_folder, "template")

template_file = st.file_uploader("Upload New Template", type=['pdf', 'txt', 'docx', 'odt'], key="config_template") # Moved here

if template_file:
    file_identifier = (template_file.name, template_file.size)
    if file_identifier not in st.session_state.processed_upload_ids:
        archive_all_files_in_folder(template_folder)
        process_uploaded_file(template_file, template_folder)
        st.session_state.processed_upload_ids.append(file_identifier)
        st.success("Template updated!")
        st.rerun()

if current_template_files:
    active_template = os.path.join(template_folder, current_template_files[0])
    
    if st.button("❌ Remove Template"):
        move_to_old(active_template, os.path.join(template_folder, "old_files"))
        st.rerun()

    try:
        with open(active_template, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
        st.text_area("Preview (First 10 Lines)", "".join(lines), height=150)
    except UnicodeDecodeError:
        st.error(f"Could not display preview for '{current_template_files[0]}'. The file might be corrupted or have an unsupported encoding.")
    except Exception as e:
        st.error(f"An error occurred while reading '{current_template_files[0]}': {e}")

# System Prompt (similar to template)
st.subheader("System Prompt")
system_folder = "static_assets/system_prompt"
current_system_files = process_and_display_files(system_folder, "system_prompt")

system_file = st.file_uploader("Upload New System Prompt", type=['pdf', 'txt', 'docx', 'odt'], key="config_system") # Moved here

if system_file:
    file_identifier = (system_file.name, system_file.size)
    if file_identifier not in st.session_state.processed_upload_ids:
        archive_all_files_in_folder(system_folder)
        process_uploaded_file(system_file, system_folder)
        st.session_state.processed_upload_ids.append(file_identifier)
        st.success("System Prompt updated!")
        st.rerun()

if current_system_files:
    active_system = os.path.join(system_folder, current_system_files[0])
    
    if st.button("❌ Remove System Prompt"):
        move_to_old(active_system, os.path.join(system_folder, "old_files"))
        st.rerun()

    try:
        with open(active_system, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
        st.text_area("Preview (First 10 Lines)", "".join(lines), height=150)
    except UnicodeDecodeError:
        st.error(f"Could not display preview for '{current_system_files[0]}'. The file might be corrupted or have an unsupported encoding.")
    except Exception as e:
        st.error(f"An error occurred while reading '{current_system_files[0]}': {e}")

# Tech Library
st.subheader("Tech Library (Multiple Files, Concatenated)")
tech_folder = "static_assets/tech_library"
current_tech_files = process_and_display_files(tech_folder, "tech_library")

tech_files = st.file_uploader("Upload Tech Files", type=['pdf', 'txt', 'docx', 'odt'], key="config_tech", accept_multiple_files=True) # Moved here

if tech_files:
    newly_processed = False
    for tech_file in tech_files:
        file_identifier = (tech_file.name, tech_file.size)
        if file_identifier not in st.session_state.processed_upload_ids:
            process_uploaded_file(tech_file, tech_folder)
            st.session_state.processed_upload_ids.append(file_identifier)
            newly_processed = True
    
    if newly_processed:
        st.success(f"{len(tech_files)} tech files added!")
        st.rerun()

if current_tech_files:
    for f in current_tech_files:
        # Place button above preview
        if st.button("❌ Remove", key=f"config_remove_tech_{f}"):
            move_to_old(os.path.join(tech_folder, f), os.path.join(tech_folder, "old_files"))
            st.rerun()
        
        try:
            with open(os.path.join(tech_folder, f), 'r', encoding='utf-8') as file:
                lines = file.readlines()[:10]
            st.text_area(f"Preview {f} (First 10 Lines)", "".join(lines), height=150)
        except UnicodeDecodeError:
            st.error(f"Could not display preview for '{f}'. The file might be corrupted or have an unsupported encoding.")
        except Exception as e:
            st.error(f"An error occurred while reading '{f}': {e}")

if st.button("Clear All Tech Files"):
    for f in current_tech_files:
        move_to_old(os.path.join(tech_folder, f), os.path.join(tech_folder, "old_files"))
    st.rerun()
