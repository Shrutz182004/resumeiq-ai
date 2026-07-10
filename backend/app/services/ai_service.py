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
You are an expert ATS Resume Reviewer and Career Coach.

Compare the candidate's resume with the given Job Description.

Analyze carefully and return ONLY valid JSON.

Do NOT return markdown.
Do NOT return explanation.
Do NOT wrap JSON inside ```.

Return this exact JSON format:

{{
    "match_score": 0,
    "ats_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "missing_keywords": [],
    "strengths": [],
    "resume_improvements": [],
    "interview_probability": "",
    "overall_feedback": ""
}}

Instructions:

- Match Score should be between 0 and 100.
- ATS Score should be between 0 and 100.
- Mention only skills actually present in the resume.
- Never invent projects or experience.
- Suggest practical improvements.
- Interview probability should be one of:
    - High
    - Medium
    - Low

Resume:

{resume_text}

Job Description:

{job_description}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        return {
    "match_score": 0,
    "ats_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "missing_keywords": [],
    "strengths": [],
    "resume_improvements": [],
    "interview_probability": "",
    "overall_feedback": ""
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

def improve_bullet_point(bullet: str):
    prompt = f"""
You are an expert ATS Resume Writer.

Your job is to improve ONLY the given resume bullet point.

Rules:
- Keep it concise.
- Use strong action verbs.
- Add ATS-friendly keywords where appropriate.
- Make it achievement-oriented.
- Do NOT invent technologies or numbers.
- Return ONLY the improved bullet.
- Do not add explanations.

Bullet:

{bullet}
"""

    response = model.generate_content(prompt)

    return response.text.strip()