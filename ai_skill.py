from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_skills_with_ai(domain):

    try:
        prompt = f"""
List the top 10 most important technical skills required for a {domain}.

STRICT RULES:
- Only return skills
- No numbering
- No explanation
- No sentences
- Output MUST be comma-separated

Example:
python, sql, machine learning, data analysis
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a job market expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        skills_text = response.choices[0].message.content.lower()

        # -----------------------------
        # 🔥 CLEANING (VERY IMPORTANT)
        # -----------------------------

        # Remove numbering like "1. skill"
        skills_text = re.sub(r"\d+\.", "", skills_text)

        # Split by comma OR newline
        skills = re.split(r",|\n", skills_text)

        # Clean & remove empty
        skills = [s.strip() for s in skills if s.strip() != ""]

        # -----------------------------
        # ⚠️ SAFETY FALLBACK
        # -----------------------------
        if len(skills) < 3:
            return ["python", "sql", "excel", "communication"]

        return skills

    except Exception as e:
        print("AI Skill Generation Error:", e)
        return ["python", "sql", "excel", "communication"]