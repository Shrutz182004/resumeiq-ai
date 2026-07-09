import os
import json

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text: str):
    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the following resume and return ONLY valid JSON.

The JSON format must be:

{{
    "ats_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": []
}}

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if Gemini wraps the JSON in ```json
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


import json


def compare_resume_with_job(resume_text: str, job_description: str):
    prompt = f"""
You are an expert ATS Resume Analyzer.

Compare the resume with the job description.

Return ONLY valid JSON.

Format:

{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "missing_keywords": [],
    "suggestions": []
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "missing_keywords": [],
            "suggestions": [
                "Failed to parse AI response."
            ]
        }
def rewrite_resume(resume_text: str):
    prompt = f"""
You are an expert resume writer.

Rewrite the following resume to make it:

- ATS Friendly
- Professional
- Strong action verbs
- Better formatting
- Better project descriptions
- Better summary
- Better keyword optimization

Return ONLY the improved resume as plain text.

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    return response.text.strip()

def chat_with_resume(resume_text: str, question: str):
    prompt = f"""
You are an expert AI Resume Coach.

You have the following resume:

{resume_text}

The user asks:

{question}

Answer professionally.

If possible:

- Explain clearly.
- Give examples.
- Give actionable advice.
"""

    response = model.generate_content(prompt)

    return response.text