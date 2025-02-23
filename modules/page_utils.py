import streamlit as st

def add_logout_button():
    """Adds a logout button to the page"""
    def logout():
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Clear cache
        st.cache_data.clear()
        st.cache_resource.clear()
        # Redirect to main/login page
        st.switch_page("main.py")

    # Add logout button in the top right corner
    col1, col2 = st.columns([11, 1])
    with col2:
        if st.button("Logout", type="primary"):
            logout() 