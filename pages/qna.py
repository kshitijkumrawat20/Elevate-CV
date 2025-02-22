import streamlit as st
from modules.llm_connector import connect_llm
from modules.result_generator import chat
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

st.set_page_config(
    page_title="qna",
    # initial_sidebar_state="collapsed"
)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "conversation" not in st.session_state:
    llm = connect_llm()
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=st.session_state.memory,
        verbose=True
    )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        try:
            # Get response using conversation chain with memory
            response = st.session_state.conversation.predict(input=prompt)
            st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Add a button to clear conversation history
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.memory.clear()
    st.rerun()