
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Lifestyle Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Lifestyle Assessment Dashboard")
st.write("Overview of questionnaire responses")

file_name = "responses.csv"

if not os.path.exists(file_name):
    st.warning("No responses found. Complete the questionnaire first.")

else:
    df = pd.read_csv(file_name)

    if df.empty:
        st.info("The dataset is currently empty.")

    else:
        total_users = len(df)
        average_score = df["Score"].mean()
        highest_score = df["Score"].max()
        lowest_score = df["Score"].min()

        st.subheader("Key Performance Indicators")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Responses", total_users)
        col2.metric("Average Score", f"{average_score:.1f}/20")
        col3.metric("Highest Score", f"{highest_score}/20")
        col4.metric("Lowest Score", f"{lowest_score}/20")

        st.divider()

        st.subheader("Lifestyle Categories")

        category_counts = df["Category"].value_counts()
        st.bar_chart(category_counts)

        st.subheader("Average Score by Category")

        category_scores = df.groupby("Category")["Score"].mean()
        st.bar_chart(category_scores)

        st.subheader("All Questionnaire Responses")

        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="Download Results as CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="lifestyle_results.csv",
            mime="text/csv"
        )
