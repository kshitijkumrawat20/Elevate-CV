import streamlit as st

from modules.document_processing import load_resume
from modules.result_generator import skill_gap_findings
from modules.result_generator import ATS_calculation
import plotly.graph_objects as go

st.set_page_config(
    page_title="dashboard",
    # initial_sidebar_state="collapsed"
)
# Function to plot ATS score as a donut chart using Plotly
def plot_ats_donut(ats_score):
    fig = go.Figure(data=[go.Pie(
        values=[ats_score, 100 - ats_score],
        labels=[f"ATS Score: {ats_score}%", "Remaining"],
        hole=0.6,  # Creates the donut effect
        marker=dict(colors=["#4CAF50", "#D3D3D3"]),  # Colors
        textinfo="percent"
    )])

    fig.update_layout(
        showlegend=False,
        annotations=[dict(text=f"{ats_score}%", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)


st.title("this is dashboard page")
user_id = st.session_state.get("user_id", "user id not found")
user_datas = st.session_state.get("data_dict", "user id not found")
llm = st.session_state.get("llm", "Instance Not Found")

        
## Skill gag analysis
st.markdown("## Skill gag analysis")

# st.write(user_id['user_idd'])
job_description = user_datas[user_id['user_idd']][0]['job_description']
resume_path = user_datas[user_id['user_idd']][0]['file_name']

# st.write(job_description)
# st.write(resume_path)

resume_text = load_resume(resume_path)

# llm = connect_llm()

with st.spinner(text="Generating..."):
    skills_gaps = skill_gap_findings(job_description=job_description, resume_text=resume_text, llm=llm)
    ATS_score = ATS_calculation(job_description=job_description, resume_text=resume_text, llm=llm)
    # optimized_resume = optimize_resume(job_description=job_description, resume_text=resume_text, llm=llm)
    
    st.markdown(skills_gaps)
    st.markdown(ATS_score['content'])
    # st.markdown(optimized_resume)

if ATS_score['value']:
    plot_ats_donut(ATS_score['value'][0])