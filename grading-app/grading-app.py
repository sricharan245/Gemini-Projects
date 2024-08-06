# Field to put my JD
# upload PDF
# PDF to image --> processing --> Google Gemini Pro
# Prompts Tempalet [ Multi]

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

# genai.configure(api_key = os.getenv("GOOGLE_API_KEY")) 
genai.configure(api_key='AIzaSyATdUX_TgDjsmuNbzv9fBBMVcJ2PN3AzHA')



def setup_grading_model(input_prompt):
    model = genai.GenerativeModel('models/gemini-1.5-pro')
    response = model.generate_content(input_prompt)
    return (model, response.text)

    


def get_gemini_response(model, prompt):
    response = model.generate_content(prompt)
    return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         images = pdf2image.convert_from_bytes(uploaded_file.read())
#         first_page = images[0]

#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()
#             }
#         ]
        
#         return pdf_parts
#     else:
#         raise FileNotFoundError("file not found")
    

st.set_page_config(page_title = "Grading App")
st.header("Grading System")
assignment_context = st.text_area("Assignment context: ", key="assignment_context")
rubric_input_text = st.text_area("Rubric: ", key="rubric_input_text")
submission_to_grade = st.text_area("Submission to Grade: ", key="submission_to_grade")

# uploaded_file = st.file_uploader("upload your resume in pdf", type=["pdf"])


submit1 = st.button("Start Modeling")

# submit2 = st.button("How can I improvise my skills")

submit3 = st.button("Grade Submission")

input_prompt1 = f"""
     Act like a teacher in the field of data science who is able to read information, analyze text and give supportive feedback based on a rubric that I will give you. 
     your task is to understand the provided assignment requirements and grade student as per the rubric provided. 
     Students were given the following assignment:
        {assignment_context}.
     Here is the rubric: 
        {rubric_input_text}.
    I will then begin to give you the student work to evaluate and you will give score as per rubric provided only.
        Here is the student's work: {submission_to_grade}.
    Please evaluate above work and give score as per rubric provided only and if anything missing in the work please tell what is missing in the work as per rubric only.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, data engineering, data analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

to_grade_prompt = f"""
    Here is the submission: {submission_to_grade}
"""



class Modeling:
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-1.5-pro')
    
    def setup_grading_model(self, input_prompt):
        response = self.model.generate_content(input_prompt)
        return response.text

    def get_gemini_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text

modeling1  = Modeling()
modeling = modeling1

if submit1:

    response = modeling.setup_grading_model(input_prompt1)
    st.subheader("The Setup Response is")
    st.write(response)
    
elif submit3:
    
    response=modeling.get_gemini_response(to_grade_prompt)
    st.subheader("The Grading Response is")
    st.write(response)

