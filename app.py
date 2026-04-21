import streamlit as st
from resume_reader import extract_text_from_pdf, extract_skills_from_resume
from skill_gap import calculate_skill_gap
from llm_engine import generate_roadmap
from market_analyzer import get_all_domains
from ats_analyzer import calculate_ats_score
from database import create_table, save_user_data, get_user_history
import plotly.graph_objects as go
import re
from fpdf import FPDF

st.set_page_config(page_title="CareerMap AI 🔎", layout="wide")

# ---------- DATABASE INIT ----------
create_table()

# ---------- SESSION STATE ----------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "roadmap" not in st.session_state:
    st.session_state.roadmap = None

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# ---------- PDF FUNCTION ----------
def generate_pdf(name, domain, ats, match_score, roadmap):

    def clean_text(text):
        return text.encode('latin-1', 'ignore').decode('latin-1')

    name = clean_text(name)
    domain = clean_text(domain)
    roadmap = clean_text(roadmap)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "CareerMap AI Report", ln=True, align='C')

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Domain Selected: {domain}", ln=True)
    pdf.cell(200, 10, f"ATS Score: {ats}", ln=True)
    pdf.cell(200, 10, f"Skill Match Score: {match_score}%", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Generated Career Roadmap:", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", size=12)

    for line in roadmap.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest='S').encode('latin-1')


# ---------- UI STYLE ----------
st.markdown("""
<style>
.block-container{
padding-top:3rem;
padding-left:2rem;
padding-right:2rem;
}
[data-testid="column"]:first-child{
background-color:#f1f5f9;
padding:25px;
border-radius:14px;
border:1px solid #e2e8f0;
}

/* Normal Buttons */
div.stButton > button:first-child {
background-color:#2563eb;
color:white;
font-weight:600;
border-radius:8px;
height:3em;
}
div.stButton > button:first-child:hover {
background-color:#1d4ed8;
color:white;
}

/* Download Button */
div.stDownloadButton > button {
background-color:#2563eb;
color:white;
font-weight:600;
border-radius:8px;
height:3em;
width:100%;
}
div.stDownloadButton > button:hover {
background-color:#1d4ed8;
color:white;
}

.big-phase{
font-size:26px;
font-weight:700;
margin-bottom:6px;
}
.section-head{
font-size:20px;
font-weight:700;
margin-top:12px;
margin-bottom:4px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<h1 style='background:linear-gradient(90deg,#1E3A8A,#3B82F6);
padding:20px;border-radius:20px;color:white;'>
CareerMap AI 🔎
</h1>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1,3])

# ---------- LEFT PANEL ----------
with left_col:

    st.subheader("Upload Resume")

    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    domain_list = get_all_domains()
    domain_list.append("Other")

    selected_domain = st.selectbox("Select Target Domain", domain_list)

    custom_domain = ""

    if selected_domain == "Other":
        custom_domain = st.text_input("Enter your target domain")

    if st.button("Start Analysis", use_container_width=True):

        if uploaded_file is not None and name and email:

            uploaded_file.seek(0)

            resume_text = extract_text_from_pdf(uploaded_file)
            extracted_skills = extract_skills_from_resume(resume_text)

            final_domain = custom_domain if selected_domain == "Other" else selected_domain

            result = calculate_skill_gap(
                extracted_skills,
                final_domain
            )

            ats_result = calculate_ats_score(
                resume_text,
                extracted_skills,
                final_domain,
                result["all_required_skills"]
            )

            save_user_data(
                name,
                email,
                final_domain,
                extracted_skills,
                ats_result["ats_score"],
                result["match_percentage"]
            )

            st.session_state.user_skills = extracted_skills
            st.session_state.domain_skills = result["required_skills"]
            st.session_state.missing_skills = result["missing_skills"]
            st.session_state.match_percentage = result["match_percentage"]
            st.session_state.selected_domain = final_domain
            st.session_state.ats_result = ats_result
            st.session_state.user_name = name
            st.session_state.analysis_done = True

        else:
            st.warning("Please fill all fields and upload resume.")

    if st.button("View History", use_container_width=True):
        st.session_state.show_history = True

    if st.session_state.show_history:

        if email:
            history = get_user_history(email)
            st.subheader("Your Past Analysis")

            if history:
                for row in history:
                    domain, ats, match, time = row
                    st.write(f"📅 {time}")
                    st.write(f"🎯 Domain: {domain}")
                    st.write(f"📊 ATS Score: {ats}")
                    st.write(f"📈 Skill Match: {match}%")
                    st.markdown("---")
            else:
                st.info("No history found")

        else:
            st.warning("Enter email to view history")

# ---------- RIGHT PANEL ----------
with right_col:

    if st.session_state.analysis_done:

        user_skills = st.session_state.user_skills
        domain_skills = st.session_state.domain_skills
        missing_skills = st.session_state.missing_skills
        match_percentage = st.session_state.match_percentage
        ats_result = st.session_state.ats_result
        user_name = st.session_state.user_name
        selected_domain = st.session_state.selected_domain

        col1, col2 = st.columns([1.4,1.6])

        with col1:

            st.subheader("Skill Analysis")
            st.markdown(f"**Skill Match: {match_percentage}%**")
            st.progress(match_percentage/100)

            miss_col, req_col = st.columns(2)

            with miss_col:
                st.markdown("### Missing Skills")
                for s in missing_skills:
                    st.write("•", s)

            with req_col:
                st.markdown("### Required Skills")
                for s in domain_skills:
                    st.write("•", s)

            st.markdown("### Extracted Skills")
            st.info(", ".join(user_skills))

        with col2:

            st.subheader("Applicant Tracking System (ATS) Score Analysis")

            score = ats_result["ats_score"]

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={'suffix': "/100",'font': {'size': 42}},
                gauge={
                    'axis': {'range':[0,100]},
                    'bar': {'color':"#111",'thickness':0.18},
                    'steps':[
                        {'range':[0,40],'color':"#ef4444"},
                        {'range':[40,60],'color':"#f97316"},
                        {'range':[60,80],'color':"#facc15"},
                        {'range':[80,100],'color':"#16a34a"}
                    ],
                }
            ))

            fig.update_layout(height=320,margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Recommendation")
            st.info(ats_result["recommendation"])

        st.markdown("---")

        if st.button("Generate Career Roadmap", use_container_width=True):

            with st.spinner("Generating roadmap..."):

                st.session_state.roadmap = generate_roadmap(
                    user_skills,
                    missing_skills,
                    selected_domain
                )

        if st.session_state.roadmap:

            st.subheader("Your Personalized Career Roadmap")

            roadmap = st.session_state.roadmap
            roadmap = roadmap.replace("**","")

            match = re.search(r"Phase\s*1", roadmap)
            if match:
                roadmap = roadmap[match.start():]

            phases = re.split(r"Phase\s*\d+", roadmap)
            phase_titles = re.findall(r"Phase\s*\d+.*", roadmap)

            for i, content in enumerate(phases):

                if i == 0:
                    continue

                title = phase_titles[i-1]

                with st.expander(title, expanded=(i==1)):
                    st.markdown(content)

            pdf_file = generate_pdf(
                name=user_name,
                domain=selected_domain,
                ats=ats_result["ats_score"],
                match_score=match_percentage,
                roadmap=roadmap
            )

            st.download_button(
                label="📄 Download Full Report",
                data=pdf_file,
                file_name="CareerMap_Report.pdf",
                mime="application/pdf"
            )