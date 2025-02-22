from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders.text import TextLoader

# Define a prompt for skill gap analysis

def skill_gap_findings(job_description, resume_text, llm):
    try:
        skill_gap_prompt = PromptTemplate(
            input_variables=["resume", "job_description"],
            template="""Analyze the following resume and job description. Provide a detailed analysis in the following format:
            1. Missing Technical Skills
            2. Missing Soft Skills
            3. Experience Gaps
            4. Recommendations for Improvement

            Resume: {resume}
            Job Description: {job_description}"""
        )
        skill_gap_response = llm.invoke(skill_gap_prompt.format(resume=resume_text, job_description=job_description))
        return skill_gap_response
    except Exception as e:
        raise Exception(f"Error in skill gap analysis: {str(e)}")
    
    
def optimize_resume(job_description, resume_text, llm):
    try:
        optimization_prompt = PromptTemplate(
            input_variables=["resume", "job_description"],
            template="""Optimize the following resume for ATS systems while maintaining its original structure. Focus on:
            1. Keyword optimization
            2. Action verbs
            3. Quantifiable achievements
            4. Relevant skills highlighting

            Resume: {resume}
            Job Description: {job_description}"""
        )
        return llm.invoke(optimization_prompt.format(resume=resume_text, job_description=job_description))
    except Exception as e:
        raise Exception(f"Error in resume optimization: {str(e)}")

def ATS_calculation(job_description, resume_text, llm):
    try:
        ats_score_prompt = PromptTemplate(
            input_variables=["resume", "job_description"],
            template="""Analyze the resume against the job description and provide:
            1. Overall ATS compatibility score (0-100)
            2. Keyword match percentage
            3. Format compatibility
            4. Specific improvement suggestions

            Resume: {resume}
            Job Description: {job_description}"""
        )
        return llm(ats_score_prompt.format(resume=resume_text, job_description=job_description))
    except Exception as e:
        raise Exception(f"Error in ATS calculation: {str(e)}")