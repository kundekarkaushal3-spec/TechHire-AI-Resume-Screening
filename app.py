import streamlit as st
import pandas as pd
from recommendation import show_recommendation
from login import login, logout
# -----------------------------
# Import Custom Modules
# -----------------------------
from dashboard import show_header, show_statistics
from sidebar import sidebar
from candidate_cards import (
    show_top_candidates,
    show_candidate_details
)
from charts import (
    bar_chart,
    pie_chart
)
from skill_analytics import show_skill_dashboard
from model import (
    smart_rank,
    predict_category,
    model as embedding_model
)

from research_data.rag_generation import (
    retrieve_evidence,
    generate_analysis,
    audit_requirements,
    build_verified_report
)
from utils import (
    extract_text_from_pdf,
    extract_skills
)
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide"
)
# -----------------------------
# Session
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None

if "analysis_job_desc" not in st.session_state:
    st.session_state["analysis_job_desc"] = ""    
# -----------------------------
# Load CSS
# -----------------------------
try:
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass
# -----------------------------
# Login Check
# -----------------------------
if not st.session_state["logged_in"]:
    login()
    st.stop()
# -----------------------------
# Header
# -----------------------------
show_header()
st.info("""
👋 Welcome Recruiter!
Upload multiple resumes, enter the Job Description and let AI identify the best candidates using Sentence-BERT, Semantic Matching and Explainable AI.
""")
# -----------------------------
# Sidebar
# -----------------------------
uploaded_files, job_desc, analyze, enable_rag = sidebar()
logout()
st.sidebar.success(
    f"👤 Logged in as\n\n{st.session_state['user']}"
)
# -----------------------------
# Dashboard
# -----------------------------
if not uploaded_files:
    st.info("👈 Upload one or more PDF resumes from the left sidebar.")
    show_statistics(0)
    st.stop()
# Statistics
show_statistics(len(uploaded_files))


# -----------------------------
# Analyze Button
# -----------------------------
if analyze:
    if job_desc.strip() == "":
        st.warning("Please enter a Job Description.")
        st.stop()
    with st.spinner("Analyzing resumes using AI..."):
        resumes = []
        names = []
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resumes.append(text)
            names.append(file.name)
        # -----------------------------
        # AI Ranking
        # -----------------------------
        scores = smart_rank(
            resumes,
            job_desc
        )
        # -----------------------------
        # Prepare Results
        # -----------------------------
        results = []
        for i in range(len(resumes)):
            prediction = predict_category(
                resumes[i]
            )
            results.append({
                "Name": names[i],
                "Score": round(float(scores[i]["final"]), 2),
                "Semantic": round(float(scores[i]["semantic"]), 2),
                "Skill": round(float(scores[i]["skill"]), 2),
                "Matched": scores[i]["matched"],
                "Missing": scores[i]["missing"],
                "Category": prediction["role"],
                "Dataset Similarity": round(float(prediction["dataset_similarity"]), 2),
                "Resume": resumes[i]
            })
        df = pd.DataFrame(results)
        df = df.sort_values(
            by="Score",
            ascending=False
        )

       
        st.session_state["analysis_results"] = df.copy()
        st.session_state["analysis_job_desc"] = job_desc

        
        

        # ====================================
# Display saved analysis results on every Streamlit rerun
if st.session_state["analysis_results"] is not None:
    df = st.session_state["analysis_results"].copy()
    job_desc = st.session_state["analysis_job_desc"]

    # Initialize filtered dataframe
    # ====================================
    filtered = df.copy()
    # -----------------------------
    # RECRUITER FILTERS
    # -----------------------------
    st.subheader("📊 Recruiter Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "🔍 Search Candidate",
            key="candidate_search"
        )

    with col2:
        roles = sorted(
            df["Category"].dropna().astype(str).unique().tolist()
        )

        role_filter = st.selectbox(
            "🎯 Filter Role",
            ["All"] + roles,
            key="role_filter"
        )

    with col3:
        sort_order = st.selectbox(
            "📈 Sort Score",
            ["Highest First", "Lowest First"],
            key="score_sort"
        )

    # Start with the complete result set
    filtered = df.copy()

    # Search Candidate
    if search.strip():
        filtered = filtered[
            filtered["Name"].astype(str).str.contains(
                search.strip(),
                case=False,
                na=False
            )
        ]

    # Filter Role
    if role_filter != "All":
        filtered = filtered[
            filtered["Category"] == role_filter
        ]

    # Sort Score
    filtered = filtered.sort_values(
        by="Score",
        ascending=(sort_order == "Lowest First")
    ).reset_index(drop=True)

    # Prevent crashes when search/filter returns zero candidates
    if filtered.empty:
        st.warning(
            "🔍 No candidates found. Try another candidate name "
            "or select a different role."
        )
        st.stop()

    # -----------------------------
    # TOP CANDIDATES
    # -----------------------------
    show_top_candidates(filtered)

    st.divider()

    # ============================================
    # Recruiter Analytics Dashboard
    # ============================================
    st.subheader("📊 Recruiter Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    total_candidates = len(filtered)
    average_score = round(filtered["Score"].mean(), 2)
    highest_score = round(filtered["Score"].max(), 2)
    recommended = len(filtered[filtered["Score"] >= 75])

    with col1:
        st.metric("📄 Total Candidates", total_candidates)

    with col2:
        st.metric("⭐ Average Score", f"{average_score:.2f}%")

    with col3:
        st.metric("🏆 Highest Score", f"{highest_score:.2f}%")

    with col4:
        st.metric("🎯 Recommended", recommended)

    st.divider()

    # ============================================
    # Candidate Spotlight
    # ============================================
    st.subheader("🌟 Candidate Spotlight")

    best = filtered.iloc[0]
    left, right = st.columns([2, 1])

    with left:
        st.success("🏆 Best Matching Candidate")
        st.write(f"### 👤 {best['Name']}")
        st.write(f"🎯 **Role:** {best['Category']}")
        st.write(f"⭐ **Match Score:** {best['Score']}%")
        st.write(f"🧠 **Semantic Score:** {best['Semantic']}%")
        st.write(f"🔧 **Skill Score:** {best['Skill']}%")
        st.write(f"📂 **Dataset Match:** {best['Dataset Similarity']}%")

    with right:
        st.metric("Rank", "#1")
        st.progress(min(max(float(best["Score"]) / 100, 0), 1))

        if best["Score"] >= 75:
            st.success("✅ Recommended for Interview")
        elif best["Score"] >= 60:
            st.warning("⚠ Consider for Interview")
        else:
            st.error("❌ Low Match")

    # -----------------------------
    # CHARTS
    # -----------------------------
    c1, c2 = st.columns(2)

    with c1:
        bar_chart(filtered)

    with c2:
        pie_chart(filtered)

    st.divider()
    # =====================================
    # Professional Candidate Ranking Table
    # =====================================
    st.subheader("🏆 Candidate Ranking")
    table = filtered.copy()
    # Rank
    table.insert(0, "Rank", range(1, len(table)+1))
    # Recommendation
    recommendation = []
    for score in table["Score"]:
        if score >= 90:
            recommendation.append("🌟 Strong Hire")
        elif score >= 75:
            recommendation.append("👍 Hire")
        elif score >= 60:
            recommendation.append("⚠ Consider")
        else:
            recommendation.append("❌ Reject")
    table["Recommendation"] = recommendation
    # Remove Resume Text
    table = table.drop(columns=["Resume"], errors="ignore")
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )
    st.success(f"""
    Total Candidates : {len(table)}
    Recommended : {len(table[table['Score']>=75])}
    Rejected : {len(table[table['Score']<60])}
    """)
    st.subheader("⚔ Candidate Comparison")
    if len(filtered)>=2:
        c1,c2 = st.columns(2)
        first = filtered.iloc[0]
        second = filtered.iloc[1]
        with c1:
            st.success("🥇 Rank 1")
            st.write(first["Name"])
            st.metric("Score",f"{first['Score']}%")
            st.metric("Role",first["Category"])
        with c2:
            st.info("🥈 Rank 2")
            st.write(second["Name"])
            st.metric("Score",f"{second['Score']}%")
            st.metric("Role",second["Category"])
    st.subheader("📌 Recruiter Decision")
    best = filtered.iloc[0]
    if best["Score"]>=90:
        st.success(f"""
    Interview Recommendation
    ✅ {best['Name']}
    Strong Hire
    Proceed to Technical Round
    """)
    elif best["Score"]>=75:
        st.info(f"""
    {best['Name']}
    Suitable for Interview
    """)
    else:
        st.warning("No highly suitable candidate found.")
    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    csv = df.drop(
        columns=["Resume"]
    ).to_csv(
        index=False
    )
    st.download_button(
        "⬇ Download Results",
        csv,
        file_name="candidate_ranking.csv",
        mime="text/csv"
    )
    st.divider()
    # -----------------------------
    # Candidate Details
    # -----------------------------
    job_skills = extract_skills(
        job_desc
    )
    # =======================================
    # Skill Analytics
    # =======================================
    show_skill_dashboard(
        filtered,
        extract_skills
    )
    st.divider()
    show_candidate_details(
        filtered,
        job_skills,
        extract_skills
    )
        
    # ============================================
    # Optional RAG Evidence-Based Analysis
    # ============================================
    if enable_rag:
        selected = filtered.iloc[0]

        st.divider()
        st.subheader("🧠 RAG Evidence-Based Analysis")
        st.write(f"**Candidate:** {selected['Name']}")
        st.caption(
            "Analysis uses the selected candidate's resume text "
            "and the current job description."
        )

        try:
            with st.spinner(
                "Retrieving resume evidence and generating "
                "an explanation with local Ollama..."
            ):
                # Retrieve evidence using the existing embedding model
                rag_evidence = retrieve_evidence(
                    model=embedding_model,
                    resume_text=str(selected["Resume"]),
                    job_description=job_desc
                )

                # Check keywords against the full stored resume text
                audit_results = audit_requirements(
                    str(selected["Resume"])
                )

                # Generate the LLM explanation
                rag_analysis = generate_analysis(
                    candidate_id=str(selected["Name"]),
                    role_category=str(selected["Category"]),
                    job_description=job_desc,
                    evidence=rag_evidence
                )

                # Build the deterministic keyword-presence report
                verified_report = build_verified_report(
                    candidate_id=str(selected["Name"]),
                    role_category=str(selected["Category"]),
                    evidence=rag_evidence,
                    audit_results=audit_results
                )

            st.markdown("### Retrieved Resume Evidence")

            for number, item in enumerate(rag_evidence, start=1):
                with st.expander(
                    f"Evidence {number} — "
                    f"Similarity: {item['similarity']}%"
                ):
                    st.write(item["text"])

            st.markdown("### LLM-Generated Explanation")
            st.markdown(rag_analysis)

            st.markdown("### Verified Keyword-Presence Report")

            st.text_area(
                "Report Details",
                value=verified_report,
                height=450,
                disabled=True
            )

        except Exception as error:
            st.error(
                "RAG analysis could not be completed. "
                "Check that Ollama is running and review the error."
            )
            st.exception(error)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<center>
<h3>🤖 AI Resume Screening & Ranking Platform</h3>
Developed using
<b>Python | Streamlit | NLP | Sentence-BERT | Scikit-Learn</b>
<br><br>
© 2026 MCA Mini Project
</center>
""",
unsafe_allow_html=True)