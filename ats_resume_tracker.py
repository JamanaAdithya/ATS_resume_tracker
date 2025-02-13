from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import base64

genai.configure(api_key=os.getenv("google_API_key"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

## convert pdf to image
def input_pdf_content(uploaded_file):
    ## convert pdf to image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read()) #images will be a list of image objects ([page1_image, page2_image, ...]).
        first_page=images[0]
        
        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg", # specifies the data type as image/jpeg
                "data": base64.b64encode(img_byte_arr).decode() # convert the raw image byte array into base64 encoding and then decode the base64 encoding into "UTF-8 String"
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")
    
st.set_page_config(page_title="ATS Resume Expert📄🤖")
st.header("ATS Expert System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")
    
submit1 = st.button("Tell me about the Resume")
submit2 = st.button("How can i improve my skills?")
submit3 = st.button("Percentage Match")
submit4 = st.button("What are the keywords that are missing?")

input_prompt1 = """
    You are an Experienced Human Resource Manager with Tech Experience in the field of Data Science, Full Stack Development, Big Data Engineering, DevOps, Data Analyst. 
    Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the Strengths and weaknesses of the applicant in relation to the specified Job Role provided in the Job Description.
"""

input_prompt2 = """
    You are an Expert ATS (Applicant Tracking System) analyzer with deep experience in evaluating resumes for roles such as Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis.
    Your task is to analyze the provided resume against the uploaded job description and identify skill gaps. Provide a detailed improvement plan, including:
    Current Strengths: Skills that match the job description.
    Skill Gaps: Important skills or certifications missing from the resume.
    Improvement Plan: Clear recommendations for upskilling, such as relevant courses, certifications, or projects.
    The response should be structured, concise, and actionable.
"""

input_prompt3 = """
    You are an Skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack Development, Big Data Engineering, DevOps, Data Analyst and Deep ATS functionality.
    Your task is to evaluate the resume against the provided job description. 
    Give me the Percentage match if the resume matches the job description.
    First the output should come as Percentage and then the Keywords missing and then the changes need to be made.
    The Response should be structured good instead of just providing a paragraph.
"""
input_prompt_4 = """
    You are an Expert ATS (Applicant Tracking System) analyzer with deep experience in evaluating resumes for roles such as Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis.
    Your task is to thoroughly review the provided resume against the uploaded job description and identify the specific keywords that are missing.
    Focus on technical skills, tools, certifications, programming languages, methodologies, and industry-specific terms that are commonly expected for the role.
    Present the results clearly, structured as follows:
    Missing Keywords: List all the keywords from the job description that are not found in the resume.
    Keyword Importance: Highlight which missing keywords are critical and which are optional.
    Suggestions for Improvement: Recommend how the candidate can incorporate these keywords into their resume (e.g., skills section, project descriptions, or certifications).
    Make sure the response is concise, easy to read, and well-organized for quick action.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_content(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the Resume")
        
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_content(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_content(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the Resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_content(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the Resume")
