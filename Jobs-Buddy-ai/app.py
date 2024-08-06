################
# @author: Sri Charan Bodduna
# @date: 08/06/2024
################

from dotenv import load_dotenv
load_dotenv()

import streamlit.web.cli as stcli
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key = os.getenv("GOOGLE_API_KEY")) 

def get_gemini_response(prompt, pdf_content = None,  input = None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # print(input)
    if pdf_content != None and input != None:
        response = model.generate_content([input, pdf_content[0], prompt])
    elif pdf_content == None and input == None:
        response = model.generate_content(prompt)
    else:
        return "No Response, please check inputs.."
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        
        return pdf_parts
    else:
        raise FileNotFoundError("file not found")
    

st.set_page_config(page_title = "Jobs Buddy AI")
st.header("Jobs Buddy.AI")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume in PDF format", type=["pdf"])


subPcentMatch = st.button("Percentage Match")

subAboutResume = st.button("Tell me about Resume")

subImproveSkills = st.button("How can I improvize my Skills")


subMotivate = st.button("Motivate Me!")

subLkdnReco = st.button("Give LinkedIn Recommendation")

about_resume_prompt = """
You are an experienced Technical Recruiting Manager in the field of data science and analytics, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job descriptions.
"""
improve_skills_prompt = """
You are an technical mentor, who helps people to improve their skills in the field of data science, data analytics and data engineering. Your task is to help me to improve skills that I lack in my resume based on job description.

Please provide answer highlighting skills that I lack, then ways to improve them.
"""

pcent_match_prompt = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, data engineering, data analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

motivate_prompt = """
You are an experienced motivator who knows how to keep people's energy up even when things are difficult. I want you to give me some energising and motivational advice for feeling worried, frustrated and angry about not getting job. I want you to help me look after my mind, my body and my spirit. Give me encouragement, positivity and practical actions I can take. Present your response in markdown.
"""

lkdn_reco_prompt = """
I am currently looking for a new job as data scientist and I want to add more recommendations to my LinkedIn profile to show potential new employers that I am trustworthy and experienced. Please can you help me write a short message to people I have worked with, asking them for a recommendation. Write it as a text message of no more than 100 words.
"""


if subPcentMatch:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(pcent_match_prompt,pdf_content,input_text.lower())
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif subAboutResume:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(about_resume_prompt,pdf_content,input_text.lower())
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif subImproveSkills:
    # print (input_text)
    # print()
    # print(uploaded_file)
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(improve_skills_prompt,pdf_content,input_text.lower())
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif subMotivate:
    # pdf_content=input_pdf_setup(uploaded_file)
    response=get_gemini_response(motivate_prompt)
    st.subheader("The Response is")
    st.write(response)

elif subLkdnReco:
    response=get_gemini_response(lkdn_reco_prompt)
    st.subheader("The Response is")
    st.write(response)
   
