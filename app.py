
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="LifeBalance Assessment",
    page_icon="🌿",
    layout="centered"
)

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #F5F8F5;
}
.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #164E3B, #39866A);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 36px;
}
.hero p {
    color: #E3F1E9;
}
.section-title {
    color: #205B45;
    font-size: 21px;
    font-weight: 700;
}
div.stFormSubmitButton > button {
    background-color: #246B50;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# PDF GENERATOR
def create_pdf(name, date, total_score, category,
               category_scores, recommendations):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#205B45"),
        alignment=TA_CENTER,
        fontSize=23
    )

    story = []

    story.append(Paragraph("LifeBalance", title_style))
    story.append(Paragraph(
        "Personal Lifestyle Assessment Report",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph(
        f"<b>Name:</b> {name}",
        styles["Normal"]
    ))

    story.append(Paragraph(
        f"<b>Date:</b> {date}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        f"<b>Overall Score: {total_score}/20</b>",
        styles["Heading2"]
    ))

    story.append(Paragraph(
        f"<b>Assessment Category:</b> {category}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Category Breakdown",
        styles["Heading2"]
    ))

    table_data = [
        ["Category", "Score"],
        ["Physical Activity", f"{category_scores[0]}/5"],
        ["Sleep Quality", f"{category_scores[1]}/5"],
        ["Nutrition", f"{category_scores[2]}/5"],
        ["Hydration", f"{category_scores[3]}/5"]
    ]

    table = Table(
        table_data,
        colWidths=[300, 120]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#205B45")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Personalized Recommendations",
        styles["Heading2"]
    ))

    for recommendation in recommendations:
        story.append(Paragraph(
            f"• {recommendation}",
            styles["Normal"]
        ))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "This report is an educational demonstration. "
        "It is not a medical assessment or diagnosis.",
        styles["Italic"]
    ))

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# HEADER
st.markdown("""
<div class="hero">
    <h1>🌿 LifeBalance</h1>
    <p>Your personal lifestyle assessment</p>
    <p>Understand your daily habits and discover opportunities
    to improve your overall wellbeing.</p>
</div>
""", unsafe_allow_html=True)

st.caption("LIFESTYLE ASSESSMENT | DEMO VERSION")

# QUESTIONNAIRE
with st.form("lifestyle_form"):

    st.markdown("### 01. Physical Activity")

    exercise = st.radio(
        "How often do you exercise?",
        ["Rarely", "1–2 times per week", "3–5 times per week"]
    )

    st.divider()

    st.markdown("### 02. Sleep Quality")

    sleep = st.radio(
        "How would you rate your sleep?",
        ["Poor", "Average", "Good"]
    )

    st.divider()

    st.markdown("### 03. Nutrition")

    nutrition = st.radio(
        "How balanced is your daily diet?",
        ["Not balanced", "Somewhat balanced", "Very balanced"]
    )

    st.divider()

    st.markdown("### 04. Hydration")

    water = st.radio(
        "How often do you drink enough water?",
        ["Rarely", "Sometimes", "Regularly"]
    )

    st.divider()

    name = st.text_input("Your name")

    submitted = st.form_submit_button(
        "Calculate My Lifestyle Score",
        use_container_width=True
    )


# SCORING AND RESULTS
if submitted:

    if not name.strip():

        st.warning("Please enter your name.")

    else:

        scores = {
            "Rarely": 1,
            "1–2 times per week": 3,
            "3–5 times per week": 5,
            "Poor": 1,
            "Average": 3,
            "Good": 5,
            "Not balanced": 1,
            "Somewhat balanced": 3,
            "Very balanced": 5,
            "Sometimes": 3,
            "Regularly": 5
        }

        exercise_score = scores[exercise]
        sleep_score = scores[sleep]
        nutrition_score = scores[nutrition]
        water_score = scores[water]

        total_score = (
            exercise_score
            + sleep_score
            + nutrition_score
            + water_score
        )

        if total_score <= 8:
            category = "Needs Improvement"
        elif total_score <= 14:
            category = "Moderate"
        else:
            category = "Positive"

        recommendations = []

        if exercise_score <= 3:
            recommendations.append(
                "Physical Activity: Gradually increase your weekly movement."
            )

        if sleep_score <= 3:
            recommendations.append(
                "Sleep: Try maintaining a consistent sleep schedule."
            )

        if nutrition_score <= 3:
            recommendations.append(
                "Nutrition: Consider more balanced food choices."
            )

        if water_score <= 3:
            recommendations.append(
                "Hydration: Pay attention to regular water intake."
            )

        if not recommendations:
            recommendations.append(
                "Continue maintaining your reported positive habits."
            )

        current_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        category_scores = [
            exercise_score,
            sleep_score,
            nutrition_score,
            water_score
        ]

        # SAVE RESPONSES
        new_response = {
            "Date": current_date,
            "Name": name,
            "Exercise": exercise,
            "Exercise Score": exercise_score,
            "Sleep": sleep,
            "Sleep Score": sleep_score,
            "Nutrition": nutrition,
            "Nutrition Score": nutrition_score,
            "Hydration": water,
            "Hydration Score": water_score,
            "Total Score": total_score,
            "Category": category,
            "Recommendations": " | ".join(recommendations)
        }

        file_name = "responses.csv"

        new_df = pd.DataFrame([new_response])

        if os.path.exists(file_name):
            new_df.to_csv(
                file_name,
                mode="a",
                header=False,
                index=False,
                encoding="utf-8-sig"
            )
        else:
            new_df.to_csv(
                file_name,
                index=False,
                encoding="utf-8-sig"
            )

        # DISPLAY RESULTS
        st.divider()

        st.header(f"Your Results, {name}")

        col1, col2 = st.columns(2)

        col1.metric("Lifestyle Score", f"{total_score}/20")
        col2.metric("Assessment", category)

        st.progress(total_score / 20)

        st.subheader("Category Breakdown")

        result_data = pd.DataFrame({
            "Category": [
                "Physical Activity",
                "Sleep Quality",
                "Nutrition",
                "Hydration"
            ],
            "Score": category_scores
        })

        st.bar_chart(
            result_data.set_index("Category")
        )

        st.subheader("Personalized Recommendations")

        for recommendation in recommendations:
            st.info(recommendation)

        # GENERATE PDF
        pdf_data = create_pdf(
            name,
            current_date,
            total_score,
            category,
            category_scores,
            recommendations
        )

        st.download_button(
            label="📄 Download Your PDF Report",
            data=pdf_data,
            file_name="Lifestyle_Assessment_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.success("Your responses have been saved successfully!")

        st.caption(
            "Educational demonstration only. "
            "This is not a medical assessment or diagnosis."
        )
