import streamlit as st
import json
import os

st.set_page_config(
    page_title="user",
    initial_sidebar_state="collapsed"
)

# Directories
UPLOAD_DIR = "uploads"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
    
if "data_dict" not in st.session_state:
    st.session_state.data_dict = []
    
user_id = st.session_state.get("user_id", "user id not found")


st.sidebar.write(st.session_state.data_dict)

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
            "file_name": file_path,
            "job_description": job_description
        }
        # Ensure user_data is a dictionary to store per-user entries
        if isinstance(st.session_state.data_dict, dict):
            if user_id not in st.session_state.data_dict:
                st.session_state.data_dict[user_id] = []  # Initialize list for user
            st.session_state.data_dict[user_id].append(new_entry)
        else:
            st.session_state.data_dict = {user_id: [new_entry]}  # Initialize dict

        st.success("Resume and details saved successfully!")