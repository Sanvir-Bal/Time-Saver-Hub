import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_resume(resume):
    reader = pdf.PdfReader(resume)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

st.set_page_config("ATS Checker")
st.header("Make Sure Your Resume Is ATS (Applicant Tracking System) Friendly")
st.markdown("Scared your application to your dream job won't make it past the 1st round? Simply upload your resume and paste in the job description you’re targeting. This appr analyzes your resume to highlight any missing keywords and provides a comprehensive reflection of how well it aligns with the job requirements. This way, you can fine-tune your resume to improve your chances of passing through Applicant Tracking Systems (ATS) and getting noticed by recruiters.")

job_description = st.text_area("Paste the Job Description")
resume = st.file_uploader("Upload Your Resume", type = "pdf", help = "Please Upload The PDF")

if st.button("Submit"):
    if resume is not None:
        text = input_resume(resume)
        prompt = f"""
        Hey Act Like a skilled or very experience ATS(Application Tracking System)
        with a deep understanding of tech field,software engineering,data science ,data analyst
        and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide 
        best assistance for improving thr resumes. Assign the percentage Matching based 
        on Jd and
        the missing keywords with high accuracy
        resume:{text}
        description:{job_description}

        Please provide a list of the missing key words, and a general analysis of the resume relative to the job description alongside some reccomendations.
        If there are no missing keywords tell the user that everything looks good.
        """
        response = get_response(prompt)
        st.subheader(response)