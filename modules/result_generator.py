from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

import regex


# Define system instructions for different analysis types
SKILL_GAP_SYSTEM_INSTRUCTION = """You are an AI designed to assist with resume and job description analysis to provide actionable insights for job seekers. Based on the provided user data, generate the following structured output:
        
    Skill Gap Analysis:
    - Compare the skills in the user's resume with the skills required in the job description.
    - Identify and list the matched skills (skills present in both the resume and job description).
    - Identify and list the mismatched skills (skills required in the job description but missing in the resume).
    - Important: If no job description is provided, do not generate any output for the skill gap analysis."""

RESUME_OPTIMIZATION_SYSTEM_INSTRUCTION = """You are an expert ATS system and resume writer with extensive experience in optimizing resumes for automated screening systems.
Your task is to analyze and suggest improvements while maintaining the resume's original structure and authenticity.
    - Focus only on relevant skills and experience related to the job description.
    - Do not include generic statements or unrelated industries.
    - Keep the resume format intact (Name, Contact, Skills, Experience, Projects).
    - Use bullet points where applicable.
    - Do not add unnecessary information like open-source contributions unless relevant.
"""

ATS_ANALYSIS_SYSTEM_INSTRUCTION = """You are an advanced Applicant Tracking System (ATS) with deep understanding of how ATS software analyzes resumes.
Provide only a single line with the ATS score in exactly this format:
<SCORE>ATS SCORE</SCORE> 
Do not explain or justify the score. Do not respond to follow-up questions."""

CHAT_FEATURES = """
You are an AI career assistant. Your responses should be direct and relevant to the user's questions. When users ask about their ATS score, skills gaps, or resume optimization, refer to the Analysis Results provided.

Important instructions:
1. Keep responses concise and focused on the user's specific question
2. Only respond to the user's actual question do not create question on your own in respone, don't create any chain of thoughts
3. Answer only what is asked in minimal words 
"""
COVER_LETTER_SYSTEM_INSTRUCTION = """You are an expert career assistant with experience in crafting professional cover letters tailored to specific job descriptions. 
Your task is to generate a compelling and personalized cover letter based on the candidate’s resume and the job description. 

Guidelines:
1. Address the cover letter professionally.
2. Tailor the content to align with the job description and highlight the candidate’s most relevant skills and experience.
3. Maintain a formal and engaging tone.
4. Structure it as follows:
   - **Opening Paragraph**: Introduce the candidate and express enthusiasm for the role.
   - **Middle Paragraph(s)**: Highlight key skills, achievements, and how they align with the job.
   - **Closing Paragraph**: Express interest in an interview and gratitude for consideration.
5. Keep the length concise (around 250-400 words).
"""

def extract_optimized_resume(text):
    match = regex.search(r'Optimized Resume:\s*(.*)', text, regex.DOTALL)
    return match.group(1).strip() if match else None


def create_chat_prompt(system_instruction, human_template):
    """Helper function to create chat prompts with system and human messages"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_instruction)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

def process_ats_score_response(response):
    """Extracts an integer value from any XML-like tag in a string."""
    pattern = r"<[^>]+>(\d+)%?</[^>]+>"  # Matches any tag with an integer inside
    matches = regex.findall(pattern, response)
    return [int(match) for match in matches] if matches else None

def skill_gap_findings(job_description, resume_text, llm):
    try:
        human_template = """ 
        Generate a structured response based on the provided user data. The response should follow this format: 

        1. Matched Skills:  
        - List the skills present in both the resume and job description.  
        - Present them in bullet points for clarity.  

        2. Mismatched Skills:  
        - Identify the skills required in the job description but missing from the resume.  
        - Clearly list these skills in bullet points.  
        - If no job description is provided, skip this section.  

        3. Actionable Insights:  
        - Provide personalized recommendations on how the job seeker can bridge the skill gap.  
        - Suggest relevant courses, certifications, or projects to acquire the missing skills.  
        - If applicable, highlight transferable skills that can compensate for any gaps.  

        Ensure the output is structured, clear, and job-specific. Avoid generic responses, and focus on actionable guidance tailored to the candidate's profile.
        
        Resume: {resume_text}
        Job Description: {job_description}"""
        chat_prompt = create_chat_prompt(SKILL_GAP_SYSTEM_INSTRUCTION, human_template)
        messages = chat_prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description
        )
        response = llm.invoke(messages)
        return response.content
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
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        raise Exception(f"Error in resume optimization: {str(e)}")

def ATS_calculation(job_description, resume_text, llm):
    try:
        human_template = """Output Prompt for ATS Score Generator  

        Generate a structured ATS evaluation report based on the provided resume and job description. The output should follow this format and must enclosed the score within <SCORE>ATS SCORE</SCORE>.

        1. ATS Score:  
        - Provide a percentage-based score (0-100%) indicating the resume's compatibility with the job description. <SCORE>ATS SCORE</SCORE> 

        2. Experience Match:  
        - Assess whether the candidate's experience aligns with the job requirements.  
        - Highlight any missing experience criteria.  

        3. Formatting Compliance:  
        - Check if the resume follows ATS-friendly formatting (e.g., no images, proper headings, standard fonts).  
        - List any formatting issues that might reduce ATS readability.  

        4. Actionable Suggestions:  
        - Provide specific recommendations to improve the ATS score, such as adding missing keywords, adjusting formatting, or refining job descriptions within the resume.
        
        Resume: {resume_text}
        Job Description: {job_description}"""
        
        chat_prompt = create_chat_prompt(ATS_ANALYSIS_SYSTEM_INSTRUCTION, human_template)
        messages = chat_prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description
        )
        response = llm.invoke(messages)
        score = {"content":response, "value":process_ats_score_response(response)}
        return score
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
    
def generate_coverletter(job_description, resume_text, llm):
    try:
        human_template = """Generate a professional cover letter for the following job application, incorporating key skills and experiences from the resume.

        Resume: {resume_text}
        Job Description: {job_description}

        Ensure the cover letter is well-structured, engaging, and tailored to the job role.
        """
        
        chat_prompt = create_chat_prompt(COVER_LETTER_SYSTEM_INSTRUCTION, human_template)
        messages = chat_prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description
        )
        return llm.invoke(messages)
    except Exception as e:
        raise Exception(f"Error in cover letter generation: {str(e)}")
