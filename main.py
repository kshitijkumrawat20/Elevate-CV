import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import uuid
from modules.llm_connector import connect_llm

st.set_page_config(page_title="Home", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            </style>
            """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 40px; color: orange; font-family: monospace; font-weight: bold;'>Welcome to ElevateCV</h1>", unsafe_allow_html=True)
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

st.markdown(hide_img_fs, unsafe_allow_html=True)
with st.spinner("Configuring ...", show_time=True):
    # Initialize and store LLM in session state
    if "llm" not in st.session_state:
        st.session_state.llm = connect_llm()
    
st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Login Here</h1>", unsafe_allow_html=True)

if "user_id" not in st.session_state:
    st.session_state.user_id = {}
    
user = st.session_state.get("user_id", "user id not found")

st.sidebar.write(user)

with st.form("id"):
    username = st.text_input(" ", placeholder="@aifans", label_visibility="collapsed")
    password = st.text_input(" ", placeholder="Enter password", type="password", label_visibility="collapsed")
    unique_id = str(uuid.uuid4())[::4]
    
    submitted = st.form_submit_button("Login", type="tertiary", use_container_width=False)

if submitted:
    if not username or not password:
        st.error("Missing username or password")
    else:
        st.session_state.user_id = {
            "username":username,
            "userpass":password,
            "user_idd":unique_id,
        }
            
    st.switch_page("pages/user.py")
    
add_vertical_space(7)
st.divider()
c1, c2, _, _, _ = st.columns(5)
c1.markdown("AI Powered by IMB Granite Models")
c1.image("logo/ibm.png", width=100)
c2.markdown("Hackathon organized by")
c2.image("logo/lablab.png", width=100)