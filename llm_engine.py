from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_roadmap(user_skills, missing_skills, target_domain):

    prompt = f"""
You are an expert AI career mentor.

Create a **practical learning roadmap** for a **student/fresher or anyone** who wants to become a specialist and get a job role in **{target_domain}**.
Current Skills:
{user_skills}

Missing Skills:
{missing_skills}

RULES:
• Divide the roadmap into **5 phases**
• Each phase should represent **1–2 weeks**
• Mention **approximate weekly study hours (6–12 hrs/week)**
• Keep content **concise and structured**
• Avoid long paragraphs and focus on short and consice content
• Use **numbered lists or short bullets**

For EACH phase include these sections:

Phase Title  
Example: Phase 1 (Week 1–2): Foundations

Objective  
Short explanation of what this phase focuses on.

Learning Steps  
Numbered steps of what to study.

Skills to Learn  
Numbered list of specific skills we are going to learn.

Tools to Practice  
Bullet list of tools or technologies to use while studying these skills.

Project Idea  
One simple practical project or task to help in practical knowledge.

YouTube Resources  
• Video Title – Channel Name

Websites / Courses  
• Platform – Course

Ensure the roadmap is **clear, beginner-friendly, and realistic for weekly study schedules.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional career mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content