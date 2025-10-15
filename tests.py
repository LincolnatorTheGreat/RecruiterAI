import unittest
import os
import shutil
from file_utils import read_file, get_latest_file, move_to_old, convert_to_md, archive_old_letters, get_tech_library_content
from generate_letter import generate_letter

class TestFileUtils(unittest.TestCase):

    def setUp(self):
        # Create dummy files and folders for testing
        os.makedirs("test_folder", exist_ok=True)
        with open("test_folder/test.txt", "w") as f:
            f.write("This is a test file.")
        from fpdf import FPDF

        # Create a dummy PDF file
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="This is a test pdf.", ln=1, align="C")
        pdf.output("test_folder/test.pdf")

    def tearDown(self):
        # Clean up the dummy files and folders
        shutil.rmtree("test_folder")

    def test_read_file(self):
        # Test reading a text file
        content = read_file("test_folder/test.txt")
        self.assertEqual(content, "This is a test file.")

        # Test reading a pdf file
        content = read_file("test_folder/test.pdf")
        self.assertIn("This is a test pdf.", content)

    def test_get_latest_file(self):
        # Test getting the latest file
        latest_file = get_latest_file("test_folder")
        self.assertEqual(latest_file, os.path.join("test_folder", "test.pdf"))

    def test_move_to_old(self):
        # Test moving a file to the old folder
        os.makedirs("test_folder/old_files", exist_ok=True)
        move_to_old("test_folder/test.txt", "test_folder/old_files")
        self.assertFalse(os.path.exists("test_folder/test.txt"))
        self.assertTrue(os.path.exists("test_folder/old_files/test.txt"))

    def test_convert_to_md(self):
        # Test converting a file to markdown
        md_path = convert_to_md("test_folder/test.txt", "test_folder")
        self.assertTrue(os.path.exists(md_path))
        with open(md_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.")

from unittest.mock import patch

class TestGenerateLetter(unittest.TestCase):

    def setUp(self):
        # Create dummy files and folders for testing
        os.makedirs("candidate_inputs/jd", exist_ok=True)
        os.makedirs("candidate_inputs/resume", exist_ok=True)
        os.makedirs("static_assets/message_template", exist_ok=True)
        os.makedirs("static_assets/system_prompt", exist_ok=True)
        os.makedirs("static_assets/tech_library", exist_ok=True)
        with open("candidate_inputs/jd/JD.txt", "w") as f:
            f.write("This is a job description.")
        with open("candidate_inputs/resume/resume.txt", "w") as f:
            f.write("This is a resume.")
        with open("static_assets/message_template/message_template.txt", "w") as f:
            f.write("This is a message template.")
        with open("static_assets/system_prompt/system_prompt.txt", "w") as f:
            f.write("This is a system prompt.")
        with open("static_assets/tech_library/tech_library.txt", "w") as f:
            f.write("This is a tech library.")

    def tearDown(self):
        # Clean up the dummy files and folders
        shutil.rmtree("candidate_inputs")
        shutil.rmtree("static_assets")

    @patch('generate_letter.call_gemini')
    def test_generate_letter(self, mock_call_gemini):
        # Mock the call_gemini function
        mock_call_gemini.return_value = "This is a generated letter."

        # Test generating a letter
        letter = generate_letter("candidate_inputs/resume/resume.txt")
if __name__ == '__main__':
    unittest.main()
