from modules.document_processing import load_resume
from modules.llm_connector import connect_llm
from modules.result_generator import optimize_resume, skill_gap_findings, ATS_calculation
import json 
import os 
json_file_path = os.path.join("data", "user_data.json")

with open(json_file_path, "r") as file:
    data = json.load(file)
    
#  load the job description 

Job_description = data[0]["job_description"]

# Process the document first 
uploads_dir = "uploads"
files = [f for f in os.listdir(uploads_dir) if f.endswith(".pdf")]
if files:
    # Sort files by modification time (latest file first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(uploads_dir, x)), reverse=True)
    
    # Get the most recently uploaded file
    resume_path = os.path.join(uploads_dir, files[0])
    print("Latest Resume Path:", resume_path)
else:
    print("No PDF files found in uploads folder!")

resume_text = load_resume(resume_path)

# print(resume_text)


## connect our LLM 
llm = connect_llm()
# finding skills gaps 
skills_gaps = skill_gap_findings(job_description=Job_description, resume_text=resume_text, llm=llm)
print("--------------------Skill Gaps-------------------------------")
print(skills_gaps)
print("--------------------ATS calculation-----------------------------")
# finding ATS score 
ATS_score = ATS_calculation(Job_description, resume_text, llm)
print(ATS_score)
print("----------------------Optimized RESUME------------------------------")
# Fetch optimized RESUME 
optimized_resume = optimize_resume(Job_description, Job_description, llm)
print(optimized_resume)
