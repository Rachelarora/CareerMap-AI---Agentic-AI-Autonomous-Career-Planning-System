import pdfplumber
import io

# -----------------------------
# Extract Text from PDF
# -----------------------------

def extract_text_from_pdf(uploaded_file):
    text = ""

    file_bytes = uploaded_file.read()

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + " "

    return text

# -----------------------------
# Extract Skills from Text
# -----------------------------

def extract_skills_from_resume(text):

    skills_list = [
        "python", "sql", "machine learning", "deep learning",
        "excel", "power bi", "tableau",
        "pandas", "numpy", "statistics",
        "java", "c++", "react", "node js",
        "html", "css", "javascript",
        "django", "flask",
        "linux", "aws", "docker",
        "kubernetes", "tensorflow", "pytorch"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
