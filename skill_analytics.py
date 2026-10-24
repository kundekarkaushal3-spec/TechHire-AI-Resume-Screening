import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

def show_skill_dashboard(df, extract_skills):

    st.subheader("📊 Skill Analytics Dashboard")

    all_skills = []

    for resume in df["Resume"]:

        skills = extract_skills(resume)

        all_skills.extend(skills)

    if len(all_skills) == 0:

        st.warning("No skills detected.")

        return

    counter = Counter(all_skills)

    skill_df = pd.DataFrame(

        counter.items(),

        columns=["Skill","Count"]

    )

    skill_df = skill_df.sort_values(

        by="Count",

        ascending=False

    )

    c1,c2 = st.columns([2,1])

    with c1:

        fig = px.bar(

            skill_df,

            x="Skill",

            y="Count",

            color="Count",

            text="Count",

            title="Top Skills Found"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with c2:

        st.write("### 🔥 Top 10 Skills")

        top = skill_df.head(10)

        for _, row in top.iterrows():

            st.success(

                f"{row['Skill']} ({row['Count']})"

            )