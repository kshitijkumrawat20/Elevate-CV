import streamlit as st
from modules.llm_connector import connect_llm
from modules.result_generator import chat, CHAT_FEATURES
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from markdownlit import mdlit


st.set_page_config(
    page_title="qna",
    # initial_sidebar_state="collapsed"
)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Get analysis results from session state
    skills_gaps = st.session_state.get('skills_gaps', 'Not available')
    ats_score = st.session_state.get('ATS_score', 'Not available')
    
    # Create enhanced system message with analysis results
    enhanced_context = f"""
        {CHAT_FEATURES}

        Analysis Results:
        - Skills Gaps: {skills_gaps}
        - ATS Score: {ats_score}

        Instructions:
        - Do NOT repeat the user's question.
        - Only provide concise and helpful answers.
        """

    
    # Add enhanced system message at initialization
    st.session_state.messages.append({"role": "system", "content": enhanced_context})

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "conversation" not in st.session_state:
    llm = connect_llm()
    
    # Create a prompt template that includes the system message
    template = f"""
        {CHAT_FEATURES}

        Analysis Results:
        - Skills Gaps: {st.session_state.get('skills_gaps', 'Not available')}
        - ATS Score: {st.session_state.get('ATS_score', 'Not available')}

        Current conversation:
        {{history}}

        Human: {{input}}
        Assistant:
        """

    
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )
    
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=st.session_state.memory,
        prompt=prompt,
        verbose=True
    )

# Display chat history (skip system message in display)
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system message
        with st.chat_message(message["role"]):
            mdlit(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        mdlit(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("", show_time=True):
            try:
                # Get response using conversation chain with memory
                response = st.session_state.conversation.predict(input=prompt)
                mdlit(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

# Add a button to clear conversation history
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = [{"role": "system", "content": CHAT_FEATURES}]  # Keep system message
    st.session_state.memory.clear()
    st.rerun()