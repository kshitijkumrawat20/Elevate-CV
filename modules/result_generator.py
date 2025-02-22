from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate


# Define system instructions for different analysis types
SKILL_GAP_SYSTEM_INSTRUCTION = """You are an expert ATS system and career counselor with deep knowledge of various industries and job requirements. 
Your task is to analyze resumes against job descriptions and provide a simple respone with skills, technology, or programming language in the following example format and dont add any output just one line:
    skill gaps : Java, Jenkins, Terraform 
Do not explain, justify, or have a conversation. Just provide the one-line response."""

RESUME_OPTIMIZATION_SYSTEM_INSTRUCTION = """You are an expert ATS system and resume writer with extensive experience in optimizing resumes for automated screening systems.
Your task is to analyze and suggest improvements while maintaining the resume's original structure and authenticity."""

ATS_ANALYSIS_SYSTEM_INSTRUCTION = """You are an advanced Applicant Tracking System (ATS) with deep understanding of how ATS software analyzes resumes.
Provide only a single line with the ATS score in exactly this format:
ATS score = XX
Do not explain or justify the score. Do not respond to follow-up questions."""

CHAT_FEATURES = """
You are an AI career assistant. Your responses should be direct and relevant to the user's questions. When users ask about their ATS score, skills gaps, or resume optimization, refer to the Analysis Results provided.

Important instructions:
1. Keep responses concise and focused on the user's specific question
2. Only respond to the user's actual question do not create question on your own in respone, dont create any chain of thoughts
3. Answer only what is asked in minimal words 
"""

def create_chat_prompt(system_instruction, human_template):
    """Helper function to create chat prompts with system and human messages"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_instruction)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

def process_skill_gaps_response(response):
    """Extract the skill gaps line from the response"""
    lines = response.split('\n')
    for line in lines:
        if line.lower().strip().startswith('skill gaps :'):
            return line.strip()
    return response.strip()

def process_ats_score_response(response):
    """Extract the ATS score line from the response"""
    lines = response.split('\n')
    for line in lines:
        if line.lower().strip().startswith('ats score ='):
            return line.strip()
    return response.strip()

def skill_gap_findings(job_description, resume_text, llm):
    try:
        human_template = """Compare the following resume with the job description and list only the missing skills. 
        Provide exactly one line starting with 'skill gaps : ' followed by comma-separated skills.
        
        Resume: {resume_text}
        Job Description: {job_description}"""
        chat_prompt = create_chat_prompt(SKILL_GAP_SYSTEM_INSTRUCTION, human_template)
        messages = chat_prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description
        )
        response = llm.invoke(messages)
        return process_skill_gaps_response(response)
    except Exception as e:
        raise Exception(f"Error in skill gap analysis: {str(e)}")

def optimize_resume(job_description, resume_text, llm):
    try:
        human_template = """Optimize the following resume for ATS systems while maintaining its original structure. Focus on:
        1. Keyword optimization
        2. Action verbs
        3. Quantifiable achievements
        4. Relevant skills highlighting

        Resume: {resume_text}
        Job Description: {job_description}"""
        
        chat_prompt = create_chat_prompt(RESUME_OPTIMIZATION_SYSTEM_INSTRUCTION, human_template)
        messages = chat_prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description
        )
        return llm.invoke(messages)
    except Exception as e:
        raise Exception(f"Error in resume optimization: {str(e)}")

def ATS_calculation(job_description, resume_text, llm):
    try:
        human_template = """Calculate the ATS compatibility score (0-100) for this resume.
        Provide exactly one line in the format: ATS score = XX
        
        Resume: {resume_text}
        Job Description: {job_description}"""
        
        chat_prompt = create_chat_prompt(ATS_ANALYSIS_SYSTEM_INSTRUCTION, human_template)
        messages = chat_prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description
        )
        response = llm.invoke(messages)
        return process_ats_score_response(response)
    except Exception as e:
        raise Exception(f"Error in ATS calculation: {str(e)}")
    
def chat(text, llm):
    try:
        chat_prompt = create_chat_prompt(CHAT_FEATURES, text)
        formatted_prompt = chat_prompt.format_messages()
        response = llm.invoke(formatted_prompt)
        return response
    except Exception as e:
        raise Exception(e)