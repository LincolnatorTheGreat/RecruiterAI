# RecruiterAI Project Documentation

## Project Overview
RecruiterAI is a Python-based tool designed to automate the creation of personalized outreach letters for technical recruiters. It uses the Google Gemini API to generate letters based on job descriptions, candidate resumes, a message template, system prompt, and a library of company technology descriptions. The app has a simple web interface built with Streamlit, allowing users to upload files, configure static assets, and generate letters in batches.

The project is beginner-friendly, focusing on Python fundamentals like file I/O, API calls, and UI development. It's "agentic" in that it automates a workflow: input processing, AI generation, and output archiving.

## Features
- **Batch Generation**: Process up to 5 resumes at a time to stay under API limits.
- **File Management**: Automatic conversion to .md for consistency, archiving old files to `old_files/` subfolders.
- **UI Navigation**: Home page for uploads/generation, config page for static updates.
- **Display and Copy**: Letters displayed with clipboard copy buttons (using JS).
- **Disabling During Processing**: Buttons grey out during generation to prevent errors.
- **Regeneration**: Used resumes can be regenerated if not removed.

## Architecture and Process Flow
The app is structured as a multipage Streamlit application with a backend for logic.

### Architecture
- **Frontend (Streamlit)**:
  - `app.py`: Home page - Uploads, generation, display.
  - `pages/config.py`: Config page - Update static files.
- **Backend**:
  - `generate_letter.py`: API calls, file reading, prompt building, archiving.
- **Storage**: Folders for inputs/statics/outputs. No database—disk-based persistence.
- **AI Integration**: Gemini API for letter generation (prompt-based).

### Process Flow
1. **Startup**: Run `streamlit run app.py`. Streamlit hosts at `localhost:8501`.
2. **Uploads**:
   - User uploads JD/resume (home) or static files (config).
   - Save temp file, convert to .md (text extraction), move original to old_files.
3. **Generation (Home)**:
   - Click "Generate": Disable buttons, fill active_resumes (move 5 recent from regular).
   - Archive old letters.
   - For each active resume: Read files, build prompt, call Gemini, save .txt with name/timestamp.
   - Re-enable buttons, display letters with copy.
4. **Display**: Scan folders on every run (rerun on interaction) to show files.
5. **Config**: Update statics, similar upload/conversion.
6. **Removal**: Buttons move to old_files.

Flow Diagram (text):
```
User Upload -> Save & Convert to .md -> Move Original to old_files
Generate Button -> Disable UI -> Fill Active (5 recent) -> Archive Old Letters -> AI Call per Resume -> Save .txt -> Re-enable UI -> Display
```

## Installation and Setup
1. **Prerequisites**: Make sure you have Python 3.x installed.
2. **Run Setup Script**:
    - For Linux, run: `bash setup_linux.sh`
    - For Windows, run: `powershell.exe -ExecutionPolicy Bypass -File .\setup_windows.ps1`
   This will create a virtual environment, install the required dependencies from `requirements.txt`, prompt you to set your `GEMINI_API_KEY_RECAI`, and create a desktop shortcut.
3. **Run**: Use the desktop shortcut or run the appropriate startup script.

## Usage
- Home: Upload JD (one), resumes (multiple). Generate batch. Copy/remove as needed.
- Config: Update template/prompt/tech (multiple for tech, concatenated).
- Maintenance: Add prints for debug. Upgrade Streamlit/Gemini via pip.

## Dependencies
Dependencies are listed in the `requirements.txt` file.

## Folder Structure
- `app.py`: Home page.
- `pages/config.py`: Config page.
- `generate_letter.py`: Backend.
- `candidate_inputs/jd/`: JD files (.md).
- `candidate_inputs/resume/`: Regular resumes (.md).
- `candidate_inputs/resume/active_resumes/`: Used resumes (.md).
- `static_assets/message_template/`: Template (.md).
- `static_assets/system_prompt/`: Prompt (.md).
- `static_assets/tech_library/`: Tech files (.md, concatenated).
- `outputs/`: Generated letters (.txt).
- `*/old_files/`: Archives.

## Maintenance and Upgrades
- **Debug**: Add `print("Step: X")` in code, check PowerShell.
- **Upgrade Gemini**: Update model name in backend if new versions.
- **Add Formats**: Extend `read_file` for .docx (use docx lib, pip install python-docx).
- **Scale**: Increase batch limit if paid API.
- **Security**: Don't hardcode key; use env.
- **Tests**: Run backend standalone (if __name__ == "__main__").
- **Version Control**: Use Git for changes.

## Troubleshooting
- No Generation: Check prints for "No JD" or API error (key invalid?).
- Files Not Showing: Ensure .md, scan logic correct.
- Navigation: Use manual links if sidebar fails (folder misspelled?).
- Errors: Read tracebacks bottom-up. Google "Streamlit [error]".

For questions, add issues if on GitHub. Project created October 12, 2025.

