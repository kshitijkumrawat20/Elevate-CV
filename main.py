import streamlit as st
import time


if st.button("Login"):
    time.sleep(2)
    st.toast(":green[Files saved]", icon="✨")
    st.page_link("pages/user.py")