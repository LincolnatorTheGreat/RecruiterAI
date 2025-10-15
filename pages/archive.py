import streamlit as st
import os
import shutil # Not strictly needed for archive.py, but good to have if moving files is ever considered
import datetime # Not strictly needed for archive.py

# Helper function to list files and create download buttons
def display_folder_contents(folder_path, title):
    st.subheader(title)
    if not os.path.exists(folder_path) or not os.listdir(folder_path):
        st.info(f"No files found in {folder_path}")
        return

    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

    if files:
        for f in files:
            file_path = os.path.join(folder_path, f)
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.markdown(f"- {f}")
            with col2:
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Download",
                        data=file,
                        file_name=f,
                        mime="application/octet-stream",
                        key=f"download_{title.replace(' ', '_')}_{f}"
                    )
    else:
        st.info(f"No files found in {folder_path}")

st.title("🗄️ Archive and Asset Browser")
st.markdown("Browse and download all archived and active asset files.")

# List of folders to display
folders_to_display = {
    "Job Descriptions (Active)": "candidate_inputs/jd",
    "Job Descriptions (Old Files)": "candidate_inputs/jd/old_files",
    "Resumes (Active)": "candidate_inputs/resume",
    "Resumes (Old Files)": "candidate_inputs/resume/old_files",
    "Message Templates (Active)": "static_assets/message_template",
    "Message Templates (Old Files)": "static_assets/message_template/old_files",
    "System Prompts (Active)": "static_assets/system_prompt",
    "System Prompts (Old Files)": "static_assets/system_prompt/old_files",
    "Tech Library (Active)": "static_assets/tech_library",
    "Tech Library (Old Files)": "static_assets/tech_library/old_files",
    "Generated Letters (Outputs)": "outputs",
    "Generated Letters (Old Files)": "outputs/old_files",
}

for title, path in folders_to_display.items():
    display_folder_contents(path, title)

st.markdown("---")
st.caption("Archive Browser | RecruiterAI")