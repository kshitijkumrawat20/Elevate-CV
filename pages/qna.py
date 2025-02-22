import streamlit as st
from modules.llm_connector import connect_llm
llm = connect_llm()

st.set_page_config(
    page_title="qna",
    # initial_sidebar_state="collapsed"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        # Prepare conversation history in the format your LLM expects
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        
        try:
            # Since WatsonX doesn't support streaming by default (as per your connector),
            # we'll handle the response differently
            response = llm.invoke(prompt)  # You might need to adjust this based on your LLM's API
            st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")