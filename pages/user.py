import streamlit as st
import json
import os


st.set_page_config(
    page_title="user",
    initial_sidebar_state="collapsed"
)


# Directories
UPLOAD_DIR = "uploads"
DATA_FILE = "data/user_data.json"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            user_data = json.load(f)
        except json.JSONDecodeError:
            user_data = []
else:
    user_data = []

with st.form("user_data", border=False):
    user_name = st.text_input(" ", placeholder="John Deo", label_visibility="collapsed")
    job_role = st.text_input(" ", placeholder="Software engineer, Data scientist ...", label_visibility="collapsed")
    
    uploaded_resume = st.file_uploader(" ", label_visibility="visible", type=['PDF'], help="Upload your latest resume.")
    job_description = st.text_area(" ", placeholder="Type or Paste job description", label_visibility="collapsed")
    
    submitted = st.form_submit_button("Save", type="tertiary", use_container_width=True)

if submitted:
    if not user_name or not job_role or not uploaded_resume or not job_description:
        st.error("Please fill all fields and upload a resume.")
    else:
        # Format filename: userName_resumeName.pdf
        original_filename = uploaded_resume.name
        new_filename = f"{user_name.replace(' ', '_')}_{original_filename}"

        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())

        # Save user details to JSON
        new_entry = {
            "name": user_name,
            "role": job_role,
            "file_name": new_filename,
            "job_description": job_description
        }
        user_data.append(new_entry)

        with open(DATA_FILE, "w") as f:
            json.dump(user_data, f, indent=4)

        st.success("Resume and details saved successfully!")