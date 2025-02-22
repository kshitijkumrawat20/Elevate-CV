import streamlit as st

from modules.document_processing import load_resume
from modules.llm_connector import connect_llm
from modules.result_generator import optimize_resume
from modules.result_generator import skill_gap_findings
from modules.result_generator import ATS_calculation

st.set_page_config(
    page_title="dashboard",
    # initial_sidebar_state="collapsed"
)

st.title("this is dashboard page")
user_id = st.session_state.get("user_id", "user id not found")
user_datas = st.session_state.get("data_dict", "user id not found")

# with st.container(key="qnas"):
#     col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
#     with col1:
#         st.subheader("Practice question and answer")
#         # st.video(data="data/SampleVideo_1280x720_1mb.mp4", muted=True, autoplay=True)
#         st.page_link(page='pages/qna.py', label="Interview Questions", use_container_width=True)
#     with col2:
#         st.subheader("resume")
#         # st.video(data="data/SampleVideo_1280x720_1mbcopy.mp4", muted=True, autoplay=True)
#         st.page_link(page='pages/resumecover.py', label="Generate Resume", use_container_width=True)
        
## Skill gag analysis
st.markdown("## Skill gag analysis")

# st.write(user_id['user_idd'])
job_description = user_datas[user_id['user_idd']][0]['job_description']
resume_path = user_datas[user_id['user_idd']][0]['file_name']

# st.write(job_description)
# st.write(resume_path)

resume_text = load_resume(resume_path)

llm = connect_llm()

with st.spinner(text="Generating..."):
    skills_gaps = skill_gap_findings(job_description=job_description, resume_text=resume_text, llm=llm)
    ATS_score = ATS_calculation(job_description=job_description, resume_text=resume_text, llm=llm)
    optimized_resume = optimize_resume(job_description=job_description, resume_text=resume_text, llm=llm)
    
    # Store results in session state
    st.session_state.skills_gaps = skills_gaps
    st.session_state.ATS_score = ATS_score
    st.session_state.optimized_resume = optimized_resume
    
    st.markdown(skills_gaps)
    st.markdown(ATS_score)
    st.markdown(optimized_resume)
