# Resume Document Logic Path in RecruiterAI

This document explains the complete logic path for resume documents in the RecruiterAI project, from upload to generation and archiving. It includes the architecture of the `active_resumes` folder and how it fits into the overall system. The project uses Python with Streamlit for the UI, and folders for persistence.

## Overview
Resumes are uploaded, converted, displayed, processed in batches, and archived. The system ensures batch processing (up to 5 at a time) to avoid API limits, with regeneration possible for used resumes. All resumes are converted to .md for consistency.

## Folder Architecture
Resumes are stored in `candidate_inputs/resume/`. Key subfolders:
- **regular resumes**: Main folder for new uploads ( `candidate_inputs/resume/` , excluding subfolders).
- **active_resumes**: Subfolder for used/generated resumes ( `candidate_inputs/resume/active_resumes/` ). This holds resumes that have been processed but not removed, allowing regeneration. Architecture: Flat folder with .md files, scanned on load for display (oldest first, red labeled).
- **old_files**: Archive for removed or original files ( `candidate_inputs/resume/old_files/` ).

Diagram (text-based):
```
candidate_inputs/
└── resume/
    ├── [regular resumes .md]  # New uploads, displayed newest first
    ├── active_resumes/
    │   ├── [used resumes .md]  # Generated, displayed oldest first (red)
    │
    └── old_files/
        ├── [archived resumes]  # Removed or originals
```

## Logic Path for Resumes (Step by Step)
1. **Upload**:
   - User drags/drops resumes (PDF/TXT) via Streamlit uploader on home page.
   - Saved as temp file in `candidate_inputs/resume/`.
   - Converted to .md (text extraction, write as .md).
   - Original moved to `old_files/`.
   - Success message shown.
   - Learning: Multi-file upload (`accept_multiple_files=True`), loop to process each.

2. **Display on Home Page**:
   - On load/refresh, scan `resume/` for .md (regular) and `active_resumes/` for .md (active).
   - Regular: Sorted newest first (reverse mtime).
   - Active: Sorted oldest first (mtime), red labeled " (Generated)".
   - If no files, nothing shown.
   - Learning: `os.listdir` for scanning, sorted with lambda for custom order.

3. **Generation Trigger**:
   - Click "Generate": Disable buttons, change label to "Generating...".
   - If <5 in `\active_resumes`, move recent from regular to active (up to 5).
   - Archive old letters in outputs/.
   - For each in active: Read JD/resume/statics, build prompt, call Gemini, save .txt with name/timestamp.
   - Append to `session_state` for display.
   - Re-enable buttons.
   - Learning: While loop for filling, for loop for batch, `session_state` for persistence.

4. **Regeneration**:
   - If no new regular, generate for existing active (regeneration).
   - Used stay in active until removed.
   - Learning: Conditional: If no pending, use active.

5. **Removal/Archiving**:
   - "Remove Used Resumes": Move active to `old_files` (disabled if no active).
   - "Clear Resumes": Move all regular/active to `old_files`.
   - Individual X: Move specific to `old_files`.
   - Learning: shutil.move for archiving, list comprehension for filtering.

## Technical Details
- **Conversion**: `convert_to_md` reads (PDF/TXT), writes .md, moves original.
- **API**: Gemini prompt combines all data.
- **State**: `st.session_state.generating` disables UI during process.
- **Error Handling**: Try-except in read/call, prints for debug.
- **Upgrades**: Add docx support in `read_file` (pip install python-docx, extract text).

## Dependencies
- streamlit
- google-generativeai
- PyPDF2


