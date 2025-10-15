
# Project Overview

This project, RecruiterAI, is a Python-based web application built with Streamlit. Its primary purpose is to automate the generation of personalized outreach letters to potential candidates for job openings. The application leverages the Google Gemini API to generate these letters based on a provided job description, a candidate's resume, and a set of configurable templates and prompts.

The application provides a simple and intuitive web interface for users to upload job descriptions and resumes. It then processes these inputs, interacts with the Gemini API, and presents the generated letters to the user. The application also includes a configuration page where users can manage the templates and prompts used in the letter generation process.

The project is structured as a multi-page Streamlit application. The main application file, `app.py`, handles the user interface for the home page, including file uploads and letter generation. The `pages/config.py` file implements the configuration page. The core logic for interacting with the Gemini API and generating the letters is encapsulated in the `generate_letter.py` module.

# Building and Running

To run this project, you need to have Python and the required dependencies installed. The dependencies are listed in the `readme.md` file and include `streamlit`, `google-generativeai`, and `PyPDF2`.

1.  **Install Dependencies:**
    ```bash
    pip install streamlit google-generativeai PyPDF2
    ```

2.  **Set API Key:**
    You need to set the `GEMINI_API_KEY` environment variable to your Google Gemini API key.

3.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```
    This will start the Streamlit development server, and you can access the application in your web browser at `http://localhost:8501`.

# Development Conventions

Based on the code, the following development conventions are observed:

*   **Styling:** The code follows the general Python style guidelines (PEP 8), although there is no explicit linter configuration file.
*   **Modularity:** The code is organized into modules with specific responsibilities. The Streamlit UI code is separated from the backend logic for letter generation.
*   **File Handling:** The application has a well-defined folder structure for storing input files, output files, and static assets. It also includes a mechanism for archiving old files.
*   **Error Handling:** The code includes basic error handling, such as checking for the presence of the API key and handling file reading errors.
*   **Configuration:** The application's behavior can be customized through the configuration page, which allows users to update the templates and prompts used for letter generation.
