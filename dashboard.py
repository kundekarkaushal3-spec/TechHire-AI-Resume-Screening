import streamlit as st

# ----------------------------------
# HEADER
# ----------------------------------

def show_header():

    st.markdown("""
    <div style="
        background:linear-gradient(90deg,#2563EB,#7C3AED);
        padding:45px;
        border-radius:25px;
        color:white;
        text-align:center;
        box-shadow:0px 10px 30px rgba(0,0,0,.25);
        margin-bottom:20px;
    ">

    <h1>
        🤖 AI Resume Screening & Ranking Platform
    </h1>

    <h3>
        Smart Recruitment using NLP, Sentence-BERT &
        Explainable AI
    </h3>

    <p>
        Upload • Analyze • Rank • Recommend
    </p>

    </div>
    """, unsafe_allow_html=True)

# ----------------------------------
# DASHBOARD STATS
# ----------------------------------

def show_statistics(total):

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    
    c1.metric(
        "📄 Uploaded Resumes",
        total
    )

    c2.metric(
        "🧠 Embedding Model",
        "MiniLM"
    )

    c3.metric(
        "⚡ Scoring Method",
        "Hybrid"
    )

    c4.metric(
        "🔎 RAG Analysis",
        "Optional"
    )
