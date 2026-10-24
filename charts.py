import streamlit as st
import plotly.express as px


def bar_chart(df):

    st.subheader("📊 Resume Match Scores")

    fig = px.bar(
        df,
        x="Name",
        y="Score",
        color="Category",
        text="Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def pie_chart(df):

    st.subheader("📈 Category Distribution")

    fig = px.pie(
        df,
        names="Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )