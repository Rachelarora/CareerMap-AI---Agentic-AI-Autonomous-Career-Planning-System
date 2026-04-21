import pandas as pd
from ai_skill import generate_skills_with_ai

def load_dataset():
    return pd.read_csv("cleaned_domain_skills.csv")

def get_all_domains():
    df = load_dataset()
    return df["Domain"].unique().tolist()

def get_domain_skills(selected_domain):

    df = load_dataset()

    # 🔥 Normalize input
    selected_domain_clean = selected_domain.strip().lower()

    # 🔥 Normalize dataset
    df["Domain_clean"] = df["Domain"].str.strip().str.lower()

    # 🔍 Try to match domain
    domain_row = df[df["Domain_clean"] == selected_domain_clean]

    print("Selected Domain:", selected_domain)

    # -----------------------------
    # ✅ CASE 1: FOUND IN DATASET
    # -----------------------------
    if not domain_row.empty:
        print("Using dataset for:", selected_domain)

        skills_str = domain_row["MasterSkills"].values[0]

        skills_list = skills_str.split(",")
        skills_list = [skill.strip().lower() for skill in skills_list]

        print("Dataset Skills:", skills_list)

        return skills_list

    # -----------------------------
    # 🔥 CASE 2: NOT FOUND → AI
    # -----------------------------
    else:
        print("Using AI for:", selected_domain)

        ai_skills = generate_skills_with_ai(selected_domain)

        print("AI Skills:", ai_skills)

        # ⚠️ Safety fallback
        if not ai_skills or len(ai_skills) < 3:
            print("AI failed → using fallback skills")
            return ["python", "sql", "excel", "communication"]

        return ai_skills