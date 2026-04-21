import re

def calculate_ats_score(resume_text, user_skills, selected_domain, required_skills):

    resume_text_lower = resume_text.lower()

    score = 0

    # -----------------------------
    # 1. Resume Structure (25)
    # -----------------------------
    section_keywords = {
        "summary" : ["summary","professional summary","objective","career objective","profile"],
        "education": ["education", "qualification", "academic","academics","college","university","educational background"],
        "skills": ["skills", "technical skills","soft skills","expertise","core competencies","key skills", "skill set", "technologies","competencies", "tools", "proficiencies"],
        "experience": ["experience", "work", "employment", "internship","professional experience","career history","professional background","work history"],
        "projects": ["project", "projects","academic projects","personal projects","major projects","minor projects"],
        "certifications": ["certification", "certifications", "courses","achievements","interests","licenses","awards","research","accomplishments","honors"]
    }

    found_sections = 0

    for section, keywords in section_keywords.items():
        for word in keywords:
            if word in resume_text_lower:
                found_sections += 1
                break

    structure_score = (found_sections / len(section_keywords)) * 25
    score += structure_score


    # 2. Keyword Density (20)
    
    keyword_matches = 0

    for skill in user_skills:
        if skill.lower() in resume_text_lower:
            keyword_matches += 1

    if len(user_skills) > 0:
        keyword_score = (keyword_matches / len(user_skills)) * 20
    else:
        keyword_score = 0

    score += keyword_score


    # -----------------------------
    # 3. Resume Length (15)
    # -----------------------------
    word_count = len(resume_text.split())

    if 400 <= word_count <= 900:
        length_score = 15
    elif 250 <= word_count < 400:
        length_score = 10
    elif word_count > 1000:
        length_score = 8
    else:
        length_score = 6

    score += length_score


    # -----------------------------
    # 4. Action Verbs (15)
    # -----------------------------
    action_words = [
        "developed", "built", "created", "implemented",
        "designed", "optimized", "improved", "increased",
        "reduced", "analyzed", "led"
    ]

    action_count = 0

    for word in action_words:
        if word in resume_text_lower:
            action_count += 1

    action_score = min(action_count * 2, 15)
    score += action_score


    # -----------------------------
    # 5. Skill Coverage (10)  (reduced from 15)
    # -----------------------------
    skill_count = len(user_skills)

    if skill_count >= 8:
        skill_score = 10
    elif skill_count >= 5:
        skill_score = 7
    else:
        skill_score = 4

    score += skill_score


    # -----------------------------
    # 6. DOMAIN SKILL MATCH (15) 🔥 NEW
    # -----------------------------
    matched = 0

    for skill in required_skills:
        if skill in user_skills:
            matched += 1

    if len(required_skills) > 0:
        domain_score = (matched / len(required_skills)) * 15
    else:
        domain_score = 0

    score += domain_score


    # -----------------------------
    # FINAL ATS SCORE
    # -----------------------------
    ats_score = round(score)


    # -----------------------------
    # DYNAMIC RECOMMENDATION
    # -----------------------------
    recommendation = ""

    if matched < (len(required_skills) * 0.4):
        recommendation = f"Your resume lacks important skills for {selected_domain}. Focus on adding domain-specific skills."

    elif found_sections < 4:
        recommendation = "Add sections like Projects, Certifications, or Experience to improve ATS readability."

    elif action_count < 3:
        recommendation = "Use strong action verbs like 'Developed', 'Implemented', or 'Optimized' to highlight achievements."

    elif word_count < 350:
        recommendation = "Add more project descriptions or achievements to make the resume more informative."

    elif skill_count < 6:
        recommendation = "Include more technical skills relevant to your domain to improve ATS keyword matching."

    else:
        recommendation = "Add measurable achievements such as 'Improved performance by 20%' or 'Reduced processing time by 30%' to further strengthen your resume."


    return {
        "ats_score": ats_score,
        "recommendation": recommendation
    }