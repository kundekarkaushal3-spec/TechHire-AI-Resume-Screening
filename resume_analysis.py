import streamlit as st

def analyze_resume(row):

    strengths = []
    weaknesses = []
    suggestions = []

    # Strengths
    if row["Semantic"] >= 80:
        strengths.append("Excellent semantic similarity with Job Description")

    if row["Skill"] >= 80:
        strengths.append("Most required technical skills are present")

    if row["Dataset Similarity"] >= 80:
        strengths.append("Resume closely matches successful profiles in the dataset")

    # Weaknesses
    if row["Semantic"] < 70:
        weaknesses.append("Resume content is not closely aligned with the Job Description")

    if row["Skill"] < 70:
        weaknesses.append("Several required technical skills are missing")

    # Suggestions
    for skill in row["Missing"]:
        suggestions.append(f"Learn {skill}")

    return strengths, weaknesses, suggestions


def show_resume_analysis(row):

    strengths, weaknesses, suggestions = analyze_resume(row)

    st.subheader("📋 AI Resume Analysis")

    # Strengths
    st.write("### ✅ Strengths")

    if strengths:
        for item in strengths:
            st.success(item)
    else:
        st.warning("No major strengths detected.")

    # Weaknesses
    st.write("### ⚠ Weaknesses")

    if weaknesses:
        for item in weaknesses:
            st.error(item)
    else:
        st.success("No major weaknesses detected.")

    # Suggestions
    st.write("### 📚 Learning Suggestions")

    if suggestions:
        for item in suggestions:
            st.info(item)
    else:
        st.success("No learning suggestions. Candidate is well matched.")

    # Final Decision
    st.write("### 💼 Hiring Decision")

    if row["Score"] >= 90:
        st.success("★★★★★ Strong Hire")

    elif row["Score"] >= 75:
        st.info("★★★★ Hire")

    elif row["Score"] >= 60:
        st.warning("★★★ Consider")

    else:
        st.error("★ Reject")