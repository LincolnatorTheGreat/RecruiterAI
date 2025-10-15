import streamlit as st
import os

LOG_FILE = "./logs/logs.txt"

st.title("📜 Application Logs")

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_contents = f.read()
    st.text_area("Log Content", log_contents, height=600)
else:
    st.info("No log file found. Logs will appear here once they are generated.")
