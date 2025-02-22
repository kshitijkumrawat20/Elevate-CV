import streamlit as st
import time
import uuid


if "user_id":
    st.session_state.user_id = ""
    
st.sidebar.write(st.session_state.user_id)

if st.button("Login"):
    unique_id = str(uuid.uuid4())[::4]
    st.session_state.user_id = unique_id
    st.write(st.session_state.user_id)
    time.sleep(2)
    st.toast(":green[Sucessfully logged]", icon="✨")
    st.switch_page("pages/user.py")