import streamlit as st
from report_generator import generate_report
from recommendation import show_recommendation
from resume_analysis import show_resume_analysis

# -----------------------------------------
# TOP CANDIDATE CARDS
# -----------------------------------------

def show_top_candidates(df):

    st.subheader("🏆 Top Candidates")

    top = min(3, len(df))

    cols = st.columns(top)

    medal = ["🥇", "🥈", "🥉"]

    for i in range(top):

        row = df.iloc[i]

        with cols[i]:

            st.markdown(f"""
            <div style="
            background:linear-gradient(135deg,#FFFFFF,#F8FAFC);
            padding:25px;
            border-radius:18px;
            box-shadow:0px 8px 20px rgba(0,0,0,.12);
            text-align:center;
            border:1px solid #E5E7EB;
            ">

           <h2>{medal[i]}</h2>

            <h3 style="
            color:#111827 !important;
            margin-top:10px;
            font-size:20px;
            font-weight:700;
            ">
            {row['Name']}
            </h3>

            <p style="
            font-size:16px;
            color:#374151 !important;
            margin-bottom:15px;
            font-weight:600;
            ">
            {row['Category']}
            </p>

            <h1 style="
            color:#2563EB !important;
            font-size:38px;
            font-weight:800;
            margin:10px 0;
            ">
            {row['Score']:.2f}%
            </h1>

            </div>
            """,
            unsafe_allow_html=True)


# -----------------------------------------
# CANDIDATE DETAILS
# -----------------------------------------

def show_candidate_details(df, job_skills, extract_skills):

    st.subheader("🧠 Candidate Insights")

    for index in range(len(df)):

        row = df.iloc[index]

        skills = extract_skills(row["Resume"])

        matched = row["Matched"]

        missing = row["Missing"]

        with st.expander(
            f"👤 {row['Name']}   |   {row['Score']}%"
        ):

            left, right = st.columns([2,1])

            with left:

                st.write("### 🎯 Predicted Role")

                st.success(row["Category"])

                st.write("### ⭐ Matching Skills")

                if matched:

                    for skill in matched:
                        st.success(f"✅ {skill}")

                else:

                    st.warning("No Matching Skills")

                st.write("### ❌ Missing Skills")

                if missing:

                    for skill in missing:
                        st.error(skill)

                else:

                    st.success("No Missing Skills")

                st.write("### 🔧 All Detected Skills")

                if skills:

                    skill_html = ""

                    for skill in skills:

                        skill_html += f"""
                        <span style="
                        background:#2563EB;
                        color:white;
                        padding:6px 12px;
                        margin:4px;
                        border-radius:20px;
                        display:inline-block;
                        ">
                        {skill}
                        </span>
                        """

                    st.markdown(
                        skill_html,
                        unsafe_allow_html=True
                    )

            with right:

                st.metric(
                    "Final Score",
                    f"{row['Score']:.2f}%"
                )

                st.progress(row["Score"]/100)

                st.metric(
                    "Semantic Score",
                    f"{row['Semantic']:.2f}%"
                )

                st.metric(
                    "Skill Score",
                    f"{row['Skill']:.2f}%"
                )

                st.metric(
                    "Dataset Match",
                    f"{row['Dataset Similarity']:.2f}%"
                )

                if row["Score"] >= 90:

                    st.success("🌟 Excellent Candidate")

                elif row["Score"] >= 75:

                    st.info("👍 Highly Recommended")

                elif row["Score"] >= 60:

                    st.warning("⚠ Suitable Candidate")

                else:

                    st.error("❌ Low Match")

            st.write("### 🤖 AI Explanation")

            st.success(
                f"""
            🤖 AI Decision

            ✔ Semantic Similarity : {row['Semantic']}%

            ✔ Skill Match : {row['Skill']}%

            ✔ Dataset Similarity : {row['Dataset Similarity']}%

            ✔ Predicted Role : {row['Category']}

            ✔ Final Score : {row['Score']}%
            """
            )

            show_recommendation(row)
            show_resume_analysis(row)

            # Generate PDF Report
            pdf_file = generate_report(row)

            with open(pdf_file, "rb") as f:

                st.download_button(
                    "📄 Download Candidate Report",
                    data=f,
                    file_name=f"{row['Name']}.pdf",
                    mime="application/pdf"
                )

            st.write("### 📄 Resume Preview")

            st.text_area(
                "",
                row["Resume"][:1200],
                height=220,
                key=f"resume_{index}"
            )