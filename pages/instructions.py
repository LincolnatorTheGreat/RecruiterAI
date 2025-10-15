import streamlit as st

st.title("📚 RecruiterAI User Guide")
st.markdown("---")

st.header("Welcome to RecruiterAI!")
st.write("This tool helps you quickly generate personalized outreach letters for job candidates. Follow these simple steps to get started:")

st.markdown("---")
st.header("1. Job Description (JD) Management")
st.write("This section is where you manage the Job Description for which you are recruiting.")
st.subheader("Upload a New JD:")
st.write("To upload a new Job Description:")
st.markdown("1.  Click the **'Upload JD (PDF/TXT/DOCX/ODT)'** button.")
st.markdown("2.  Select your JD file (PDF, TXT, DOCX, or ODT format) from your computer.")
st.markdown("3.  Once uploaded, the system will convert it to a readable format and display the first 25 lines as a preview.")
st.markdown("4.  The newly uploaded JD will become the **'Current JD'** used for letter generation.")
st.subheader("Current JD Preview:")
st.write("Below the uploader, you'll see the name of the currently active JD and a preview of its first 25 lines. This is the JD the AI will use to understand the role.")

st.markdown("---")
st.header("2. Candidate Resume Management")
st.write("This section allows you to upload and manage candidate resumes.")
st.subheader("Upload Resumes:")
st.write("To upload candidate resumes:")
st.markdown("1.  Click the **'Upload Resume (PDF/TXT/DOCX/ODT/MD)'** button.")
st.markdown("2.  You can select multiple resume files (PDF, TXT, DOCX, ODT, or MD format) at once.")
st.markdown("3.  Once uploaded, the system will convert them to a readable format.")
st.subheader("Used Resumes (Ready to be Regenerated):")
st.write("This list shows resumes that were previously used in a generation cycle. They are kept here for easy re-use if you need to generate new letters for them.")
st.markdown(" -   Click **'❌ Remove'** next to a resume to move it out of the active list.")
st.subheader("Available Resumes:")
st.write("This list shows all other resumes you have uploaded that are available for letter generation.")
st.markdown(" -   Click **'❌ Remove'** next to a resume to move it to the archive.")
st.subheader("Resume Control Buttons:")
st.markdown(" -   **'Remove Used Resumes'**: Moves all resumes from the 'Used Resumes' list to the archive.")
st.markdown(" -   **'Clear All Resumes'**: Moves all resumes (both 'Used' and 'Available') to the archive.")

st.markdown("---")
st.header("3. Generate Letters")
st.write("Once you have an active JD and at least one resume, you can generate personalized letters.")
st.markdown("1.  Click the **'✨ Generate Letters (Up to 5)'** button.")
st.markdown("2.  The system will move up to 5 of your 'Available Resumes' into the 'Used Resumes' section and begin generating letters.")
st.markdown("3.  A spinner will appear, indicating that letters are being generated. This might take a moment.")
st.markdown("4.  After generation, the newly created letters will appear in the **'Generated Letters'** section below.")

st.markdown("---")
st.header("4. Generated Letters")
st.write("This section displays all the letters generated in the current session.")
st.markdown(" -   Each letter is shown in an editable text box. You can make minor adjustments directly in the box.")
st.markdown(" -   To copy a letter, simply **highlight the text** within the box and press **Ctrl+C (Cmd+C on Mac)**.")
st.subheader("Clear Generated Letters:")
st.write("Clicking **'Clear Generated Letters'** will archive all currently displayed letters and clear them from the screen, making space for a new batch.")

st.markdown("---")
st.header("5. Other Pages (Sidebar)")
st.write("You can navigate to other useful pages using the sidebar on the left:")
st.markdown(" -   **'Config'**: Manage the AI's underlying templates and prompts. (Advanced users)")
st.markdown(" -   **'Archive'**: Browse and download all active and archived files (JDs, Resumes, Letters, Templates, Prompts).")

st.markdown("---")
st.header("6. Sample Letter")
st.write("Here is an example of a letter that RecruiterAI can generate:")
st.code("""
Subject: Opportunity at Mainspring Energy - Staff Mechanical Engineer

Hi [Candidate Name],

I came across your profile and was impressed with your background in mechanical engineering, particularly your experience with [Specific Skill from Resume].

At Mainspring Energy, we're developing innovative new power generation technology. Based on your experience, I thought you might be a great fit for our Staff Mechanical Engineer role.

Would you be open to a brief chat next week to discuss how your skills could align with our work?

Best,

[Your Name]
""", language="markdown")

st.markdown("---")
st.caption("RecruiterAI User Guide | Built with Streamlit & Gemini API")