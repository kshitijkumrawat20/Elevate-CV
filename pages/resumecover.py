import streamlit as st
import os
from modules.document_processing import load_resume
from markdownlit import mdlit
from modules.result_generator import generate_coverletter, optimize_resume
from toggle_button_set import toggle_button_set

st.set_page_config(
    page_title="resume",
    initial_sidebar_state="collapsed",
    layout="centered"
)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

st.markdown(hide_img_fs, unsafe_allow_html=True)

user_id = st.session_state.get("user_id", "user id not found")
user_datas = st.session_state.get("data_dict", "user id not found")
llm = st.session_state.get("llm", "Instance Not Found")

# st.write(user_id['user_idd'])
job_description = user_datas[user_id['user_idd']][0]['job_description']
resume_path = user_datas[user_id['user_idd']][0]['file_name']

resume_text = load_resume(resume_path)

# selected = toggle_button_set(
#     button_list=["Resume", "Cover Letter"],
#     default=["Resume"],
#     color="primary",
#     size="medium",
#     exclusive=True,
#     use_container_width=True,
#     key="toggle"
# )
# if "optz_cover" not in st.session_state:
#     st.session_state.optz_cover = None
# if "optz_resume" not in st.session_state:
#     st.session_state.optz_resume = None
    
# with st.spinner(text="Optimizing your resume..."):
#     if job_description and resume_text:  # Ensure inputs are provided
#         _new_resume = optimize_resume(job_description=job_description, resume_text=resume_text, llm=llm)
        
#         if _new_resume:  # Check if results are valid
#             st.session_state.optz_resume = _new_resume  # Store in session state
#             mdlit(_new_resume)  # Print result
#         else:
#             st.warning("No skill gaps found. Please check the provided resume and job description.")
#     else:
#         st.error("Missing job description or resume. Please provide both to analyze skill gaps.")


# if selected == "Cover Letter":   
#     st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Cover Letter</h1>", unsafe_allow_html=True)
# else:
#     st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Optimized Resume</h1>", unsafe_allow_html=True)
#     # Check if skill gaps are already stored
#     if st.session_state.optz_resume:
#         mdlit(st.session_state.optz_resume)  # Print stored result
        

