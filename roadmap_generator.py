def generate_roadmap(user_skills, missing_skills, target_domain):

    prompt = f"""
You are an expert AI Career Planning Agent and professional mentor.

Create a **detailed learning roadmap** for a BCA Final Year student who wants to become a **{target_domain}**.

Current Skills:
{user_skills}

Missing Skills:
{missing_skills}

Your roadmap must follow these rules:

• Divide the roadmap into **5 phases**
• Each phase should represent **1–2 months of learning**
• The roadmap should be beginner-friendly and practical
• Focus on skills required in the current job market

For EACH phase include:

1️⃣ Phase Title and Duration  
Example: Phase 1 (Month 1–2): Foundations

2️⃣ Skills to Learn  
List important skills related to the target domain.

3️⃣ Tools to Practice  
Mention industry tools or technologies.

4️⃣ Project Idea  
Give one practical project idea the student can build.

5️⃣ YouTube Learning Resources  
Provide **real YouTube channels or videos with links**.

6️⃣ Websites / Online Courses  
Suggest useful websites, courses, or free learning platforms.

Use the following format clearly:

Phase 1 (Month 1–2): Title

Skills to Learn
- ...

Tools to Practice
- ...

Project Idea
- ...

YouTube Resources
- Channel Name – Video Topic – Link

Websites / Courses
- Platform – Link

Repeat the same structure for **Phase 2, Phase 3, Phase 4, and Phase 5**.

Keep the roadmap **clear, structured, and useful for self-learning**.
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