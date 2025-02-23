import streamlit as st
from fpdf import FPDF
from modules.document_processing import load_resume
from markdownlit import mdlit
from modules.result_generator import generate_coverletter, optimize_resume
from streamlit_extras.add_vertical_space import add_vertical_space
from toggle_button_set import toggle_button_set

st.set_page_config(
    page_title="Resume Optimization",
    initial_sidebar_state="collapsed",
    layout="centered"
)

# Hide fullscreen button and unnecessary elements
st.markdown(
    '''
    <style>
    button[title="View fullscreen"] { visibility: hidden; }
    [data-testid='stHeaderActionElements'] { display: none; }
    </style>
    ''',
    unsafe_allow_html=True
)

# Retrieve user data from session state
user_id = st.session_state.get("user_id", "user id not found")
user_datas = st.session_state.get("data_dict", "user id not found")
llm = st.session_state.get("llm", "Instance Not Found")
job_description = user_datas[user_id['user_idd']]['job_description']
resume_path = user_datas[user_id['user_idd']]['file_name']

## Download function
# Download Resume as PDF
def save_pdf(content, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf_file = f"{filename}.pdf"
    pdf.output(pdf_file)
    return pdf_file


# Load resume content
resume_text = load_resume(resume_path)

# Toggle buttons for Resume and Cover Letter
selected = toggle_button_set(
    button_list=["Resume", "Cover Letter"],
    default=["Resume"],
    color="primary",
    size="medium",
    exclusive=True,
    use_container_width=True,
    key="toggle"
)

# Initialize session states if not already present
if "optz_resume" not in st.session_state:
    st.session_state.optz_resume = None

if "optz_cover" not in st.session_state:
    st.session_state.optz_cover = None

if selected == "Resume":
    st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Optimized Resume</h1>", unsafe_allow_html=True)
    add_vertical_space(1)
    
    if st.session_state.optz_resume is None:
        with st.spinner(text="Optimizing your resume..."):
            if job_description and resume_text:
                st.session_state.optz_resume = optimize_resume(job_description=job_description, resume_text=resume_text, llm=llm)
    
    if st.session_state.optz_resume:
        mdlit(st.session_state.optz_resume)
        
        resume_pdf = save_pdf(st.session_state.optz_resume, "Optimized_Resume")
        with open(resume_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Optimized Resume (PDF)",
                data=pdf_file,
                file_name="Optimized_Resume.pdf",
                mime="application/pdf",
            )
    else:
        st.warning("No optimized resume available. Please check your input.")

elif selected == "Cover Letter":
    st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Cover Letter</h1>", unsafe_allow_html=True)
    add_vertical_space(1)
    
    if st.session_state.optz_cover is None:
        with st.spinner(text="Generating cover letter..."):
            if job_description and resume_text:
                st.session_state.optz_cover = generate_coverletter(job_description=job_description, resume_text=resume_text, llm=llm)
    
    if st.session_state.optz_cover:
        mdlit(st.session_state.optz_cover)
        # Download Cover Letter as PDF
        cover_pdf = save_pdf(st.session_state.optz_cover, "Cover_Letter")
        with open(cover_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Cover Letter (PDF)",
                data=pdf_file,
                file_name="Cover_Letter.pdf",
                mime="application/pdf",
            )
    else:
        st.warning("No cover letter available. Please check your input.")
