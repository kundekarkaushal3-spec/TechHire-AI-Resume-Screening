
import streamlit as st


def sidebar():
    # Sidebar title
    st.sidebar.title("AI Resume Screening")

    # Recruiter tips
    st.sidebar.success("""
    ### 💡 Recruiter Tips

    ✔ Upload multiple resumes

    ✔ Enter complete Job Description

    ✔ Review AI Recommendation

    ✔ Compare Skill Match

    ✔ Download Results
    """)

    st.sidebar.markdown("---")

    # Upload resume PDFs
    uploaded_files = st.sidebar.file_uploader(
        "📄 Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    # Enter job description
    st.sidebar.markdown("### Job Description")

    job_desc = st.sidebar.text_area(
        "Enter Job Description",
        height=250
    )

    # Optional RAG feature
    enable_rag = st.sidebar.checkbox(
        "Generate RAG explanation for top-ranked candidate",
        value=False,
        help=(
            "Uses retrieved resume evidence and your local Ollama LLM. "
            "Generation may take a few minutes."
        )
    )

    # Analyze button
    analyze = st.sidebar.button(
        "🚀 Analyze Resumes",
        use_container_width=True
    )

    # Return all four values
    return uploaded_files, job_desc, analyze, enable_rag
