import streamlit as st
import os

def logout():
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Clear cache
    st.cache_data.clear()
    st.cache_resource.clear()
    # Redirect to main/login page
    st.switch_page("main.py") 
            
def header():
    with st.container(border=True):
        a, _, _, _, b = st.columns(5)
        if a.button("Dashboard", use_container_width=True, type="tertiary"):
            st.switch_page("pages/dashboard.py")
        if b.button("Logout", use_container_width=True, type="tertiary"):
            logout()
            
def refresh(file):
    # Define button style to match UI color
    button_style = """
        <style>
        .custom-button {
            background-color: #282a3d; /* Matching UI color */
            color: white;
            padding: 8px 15px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            font-weight: bold;
        }
        .custom-button:hover {
            background-color: #FF8C00; /* Darker blue on hover */
        }
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
    """

    # SVG Icon for Refresh
    refresh_icon = """
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="white" viewBox="0 0 16 16">
    <path d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 1 0-.908-.418A6 6 0 1 0 8 2v1z"/>
    <path d="M8 3V0L5 3h3z"/>
    </svg>
    """

    # Display button and handle state
    st.markdown(button_style, unsafe_allow_html=True)
    clicked = st.button("🔄 Re-upload", key="refresh_button")

    if clicked:
        try:
            os.remove(file)
        except:
            pass
        try:
            lkeys = ['data_dict', 'skills_gaps', 'ATS_score', 'ATS_score_content', 'optz_resume', 'optz_cover', 'messages', 'memory', 'conversation', ]
            for key in lkeys:
                if key not in ['llm', 'user_id']:
                    del st.session_state[key]
        except:
            pass
        # Redirect after clearing session state
        st.switch_page("pages/user.py")  # Ensure this page exists