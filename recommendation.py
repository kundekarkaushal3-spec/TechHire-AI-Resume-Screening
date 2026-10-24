import streamlit as st


def recommendation(score):

    if score >= 90:

        return (
            "🌟 Strong Hire",
            "Interview Immediately",
            "green"
        )

    elif score >= 75:

        return (
            "👍 Hire",
            "Recommended for Interview",
            "blue"
        )

    elif score >= 60:

        return (
            "⚠ Average",
            "Consider if required",
            "orange"
        )

    else:

        return (
            "❌ Reject",
            "Not Recommended",
            "red"
        )


def show_recommendation(row):

    status, message, color = recommendation(
        row["Score"]
    )

    st.subheader("🤖 AI Recommendation")

    if color == "green":

        st.success(status)

    elif color == "blue":

        st.info(status)

    elif color == "orange":

        st.warning(status)

    else:

        st.error(status)

    st.write(f"### 📋 Decision")

    st.write(message)

    st.write("### 📌 Why?")

    st.write(
        f"""
✔ Semantic Score : {row['Semantic']}%

✔ Skill Score : {row['Skill']}%

✔ Dataset Match : {row['Dataset Similarity']}%

✔ Final Score : {row['Score']}%
"""
    )