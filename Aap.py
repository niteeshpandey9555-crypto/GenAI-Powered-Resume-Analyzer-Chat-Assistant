#niteesh Pandey 
#LLM logic stremlit
import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from utils import load_resume

# Load env variables
load_dotenv()

# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

PROMPT = """
You are an expert resume analyzer.
Extract the following details from the resume text and return ONLY valid JSON:

{
  "Name": "",
  "Email": "",
  "Phone": "",
  "Skills": [],
  "Education": [],
  "Experience": [],
  "Projects": []
}

Resume Text:
{text}
"""

prompt = PromptTemplate(
    template=PROMPT,
    input_variables=["text"]
)

st.set_page_config(page_title="AI Resume Analyzer")
st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume_text = load_resume(file_path)

    if st.button("Analyze Resume"):
        response = llm.invoke(prompt.format(text=resume_text[:4000]))

        try:
            result = json.loads(response.content)
            st.json(result)
        except:
            st.write(response.content)
