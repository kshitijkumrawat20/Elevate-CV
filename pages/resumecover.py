import streamlit as st
from fpdf import FPDF
from modules.document_processing import load_resume
from markdownlit import mdlit
from modules.result_generator import generate_coverletter, optimize_resume, extract_optimized_resume
from streamlit_extras.add_vertical_space import add_vertical_space
from toggle_button_set import toggle_button_set
from modules.page_utils import header

st.set_page_config(
    page_title="Resume Optimization",
    initial_sidebar_state="collapsed",
    layout="centered"
)
header()
st.markdown("""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            </style>
            """, unsafe_allow_html=True)
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

# Initialize session variables
if "optz_resume" not in st.session_state:
    st.session_state.optz_resume = None
if "optz_cover" not in st.session_state:
    st.session_state.optz_cover = None

# Function to clean text and remove unsupported characters
def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

# Function to create a PDF using fpdf
def create_pdf(text, filename):
    text = clean_text(text)  # Ensure UTF-8 compatibility
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("ArialUnicode", "", "pages/Arial.ttf", uni=True)  # Use a font that supports UTF-8
    pdf.set_font("ArialUnicode", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)  # Use multi_cell to handle line breaks

    pdf_path = f"{filename}.pdf"
    pdf.output(pdf_path, "F")  # Ensure it saves in binary mode
    return pdf_path

# Function to process resume
def process_resume():
    if st.session_state.optz_resume is None:
        with st.spinner("Optimizing your resume..."):
            optimized_resume = optimize_resume(job_description, resume_text, llm)
            if optimized_resume:
                st.session_state.optz_resume = extract_optimized_resume(optimized_resume)
            else:
                st.warning("No skill gaps found. Please check the resume and job description.")
    return st.session_state.optz_resume

# Function to process cover letter
def process_cover_letter():
    if st.session_state.optz_cover is None:
        with st.spinner("Generating cover letter..."):
            cover_letter = generate_coverletter(job_description, resume_text, llm)
            if cover_letter:
                st.session_state.optz_cover = cover_letter
            else:
                st.warning("Could not generate cover letter. Check the input data.")
    return st.session_state.optz_cover

# Display Resume or Cover Letter
if selected == "Cover Letter":
    st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Cover Letter</h1>", unsafe_allow_html=True)
    cover_letter_text = process_cover_letter()
    if cover_letter_text:
        # mdlit(cover_letter_text)
        st.code(cover_letter_text, language='text', wrap_lines=True)
        pdf_path = create_pdf(cover_letter_text, "cover_letter")
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="Download Cover Letter", data=pdf_file, file_name="Cover_Letter.pdf", mime="application/pdf")
else:
    st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Optimized Resume</h1>", unsafe_allow_html=True)
    optimized_resume_text = process_resume()
    if optimized_resume_text:
        # mdlit(optimized_resume_text)
        st.code(optimized_resume_text, language='text', wrap_lines=True)
        pdf_path = create_pdf(optimized_resume_text, "optimized_resume")
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="Download Optimized Resume", data=pdf_file, file_name="Optimized_Resume.pdf", mime="application/pdf")
