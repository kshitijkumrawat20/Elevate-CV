import streamlit as st
import time
import uuid
from modules.llm_connector import connect_llm

st.set_page_config(page_title="Home", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: left; font-size: 30px; color: orange; font-family: monospace; font-weight: bold;'>Login Here</h1>", unsafe_allow_html=True)


if "user_id" not in st.session_state:
    st.session_state.user_id = {}
    
# Initialize and store LLM in session state
if "llm" not in st.session_state:
    st.session_state.llm = connect_llm()
    
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
        
    st.toast("created")
    
    st.switch_page("pages/user.py")