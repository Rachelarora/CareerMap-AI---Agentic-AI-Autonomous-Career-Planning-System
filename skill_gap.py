from market_analyzer import get_domain_skills

BAD_KEYWORDS = [
    "innovation", "strategy", "management", "leadership",
    "product", "research", "analysis", "communication",
    "planning", "documentation", "testing", "ethics"
]

def calculate_skill_gap(user_skills, selected_domain):

    # 1. Get required skills
    full_domain_skills = get_domain_skills(selected_domain)

    # 2. Normalize
    user_skills = list(set([skill.lower().strip() for skill in user_skills]))
    full_domain_skills = list(set([skill.lower().strip() for skill in full_domain_skills]))

    # 3. Filter junk skills
    filtered_skills = []
    for skill in full_domain_skills:
        if not any(bad in skill for bad in BAD_KEYWORDS):
            filtered_skills.append(skill)

    # 4. Matched + Missing (based on FULL required list)
    matched_skills = []
    missing_skills = []

    for skill in filtered_skills:
        if skill in user_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # 5. Percentage (KEEP SAME LOGIC - full domain based)
    if len(filtered_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = int((len(matched_skills) / len(filtered_skills)) * 100)

    # 6. FINAL OUTPUT (NO TOP_N ❌)
    return {
        "required_skills": filtered_skills,        # ALL required skills
        "missing_skills": missing_skills,          # subset of required
        "matched_skills": matched_skills,          # optional
        "all_required_skills": filtered_skills,
        "match_percentage": match_percentage
    }