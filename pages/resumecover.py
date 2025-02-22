import streamlit as st
import os
from modules.result_generator import generate_coverletter
st.set_page_config(
    page_title="resume",
    # initial_sidebar_state="collapsed"
)

st.title("Cover Letter")
