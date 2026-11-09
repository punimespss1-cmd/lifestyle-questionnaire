
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="LifeBalance | Lifestyle Assessment",
    page_icon="🌿",
    layout="wide"
)

# ==========================================
# 2. DESIGN
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');

:root {
    --forest: #183F32;
    --green: #3E765B;
    --cream: #F7F8F4;
    --line: #E2E9E1;
    --muted: #738078;
}

.stApp {
    background: var(--cream);
    color: #20332A;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(
        120deg,
        #173D31 0%,
        #285E47 60%,
        #54836A 100%
    );
    padding: 42px;
    border-radius: 25px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 14px 35px rgba(31,70,51,.12);
}

.hero h1 {
    color: white !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.4px;
}

.hero p {
    color: #E3EEE6 !important;
    font-size: 16px;
    line-height: 1.65;
}

.section-title {
    color: var(--forest);
    font-family: 'Manrope', sans-serif;
    font-size: 22px;
    font-weight: 800;
    padding: 12px 0 8px;
    letter-spacing: -.4px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 14px 16px 5px;
    box-shadow: 0 4px 15px rgba(30,60,42,.025);
}

div[data-testid="stRadio"] > label {
    color: #263A2F !important;
    font-size: .96rem !important;
    font-weight: 700 !important;
}

div[role="radiogroup"] {
    gap: .35rem;
}

div[role="radiogroup"] label {
    background: #FAFBF9;
    border: 1px solid #E6ECE5;
    border-radius: 11px;
    padding: .42rem .7rem;
    margin: 0 .12rem .3rem 0;
}

div[role="radiogroup"] label:hover {
    border-color: #9DB9A2;
    background: #F1F6F1;
}

div[data-testid="stTextInput"] input {
    background: white;
    border: 1px solid #DDE6DD;
    border-radius: 12px;
    min-height: 45px;
}

div.stButton > button,
div.stDownloadButton > button {
    background: #285E47;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 800;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background: #183F32;
    color: white;
    border: 0;
}

div[data-testid="stProgress"] > div {
    background: #E7EEE7;
    border-radius: 999px;
    height: 9px;
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #477D5D, #80A989);
    border-radius: 999px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 16px;
}

[data-testid="stMetricValue"] {
    color: var(--forest);
}

@media (max-width: 640px) {
    .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        padding: 26px 22px;
        border-radius: 19px;
    }

    .hero h1 {
        font-size: 32px;
    }

    div[role="radiogroup"] {
        gap: .12rem;
    }

    div[role="radiogroup"] label {
        padding: .32rem .48rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. QUESTION BANK
# ==========================================

questionnaire = {
    "Physical Activity": [
        (
            "How often do you engage in physical activity?",
            ["Never", "Rarely", "Sometimes", "Often", "Very often"]
        ),
        (
            "How often do you walk or move during the day?",
            ["Almost never", "Rarely", "Sometimes", "Often", "Very often"]
        ),
        (
            "How would you describe your weekly activity level?",
            ["Very low", "Low", "Moderate", "Active", "Very active"]
        ),
        (
            "How consistently do you maintain an exercise routine?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    ],

    "Sleep & Recovery": [
        (
            "How would you rate your overall sleep quality?",
            ["Very poor", "Poor", "Average", "Good", "Excellent"]
        ),
        (
            "How often do you wake up feeling refreshed?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        ),
        (
            "How consistent is your sleeping schedule?",
            ["Very inconsistent", "Inconsistent", "Sometimes consistent",
             "Mostly consistent", "Very consistent"]
        ),
        (
            "How often do you get enough sleep for your needs?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    ],

    "Nutrition": [
        (
            "How often do you eat fruits and vegetables?",
            ["Never", "Rarely", "Sometimes", "Often", "Daily"]
        ),
        (
            "How balanced are your daily meals?",
            ["Not balanced", "Slightly balanced", "Moderately balanced",
             "Well balanced", "Very well balanced"]
        ),
        (
            "How often do you choose minimally processed foods?",
            ["Never", "Rarely", "Sometimes", "Often", "Very often"]
        ),
        (
            "How regularly do you maintain meal routines?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    ],

    "Hydration": [
        (
            "How often do you drink water throughout the day?",
            ["Very rarely", "Rarely", "Sometimes", "Often", "Regularly"]
        ),
        (
            "How often do you carry water with you?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        ),
        (
            "How regularly do you drink water with meals?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        ),
        (
            "How attentive are you to your hydration habits?",
            ["Not attentive", "Slightly attentive", "Moderately attentive",
             "Very attentive", "Extremely attentive"]
        )
    ],

    "Lifestyle Habits": [
        (
            "How often do you take breaks during long periods of sitting?",
            ["Never", "Rarely", "Sometimes", "Often", "Very often"]
        ),
        (
            "How often do you make time for relaxation?",
            ["Never", "Rarely", "Sometimes", "Often", "Daily"]
        ),
        (
            "How would you rate your work-life balance?",
            ["Very poor", "Poor", "Average", "Good", "Excellent"]
        ),
        (
            "How consistently do you maintain healthy daily routines?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    ]
}


# ==========================================
# 4. PDF REPORT GENERATOR
# ==========================================

def create_pdf(name, date, total_score, category,
               category_scores, recommendations):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "LifeBalanceTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#205B45"),
        fontSize=27,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    story = []

    story.append(Paragraph("LifeBalance", title_style))
    story.append(Paragraph(
        "PERSONAL LIFESTYLE ASSESSMENT",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 18))

    story.append(Paragraph(
        f"<b>Participant:</b> {escape(name)}",
        styles["Normal"]
    ))

    story.append(Paragraph(
        f"<b>Assessment date:</b> {escape(date)}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 22))

    story.append(Paragraph(
        f"<b>Overall Score: {total_score}/100</b>",
        styles["Heading1"]
    ))

    story.append(Paragraph(
        f"<b>Assessment level:</b> {category}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Category Breakdown",
        styles["Heading2"]
    ))

    table_data = [["Category", "Score", "Maximum"]]

    for category_name, score in category_scores.items():
        table_data.append([
            category_name,
            str(score),
            "20"
        ])

    table = Table(
        table_data,
        colWidths=[260, 90, 90]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#205B45")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 1), (-1, -1),
         colors.HexColor("#F1F6F0"))
    ]))

    story.append(table)
    story.append(Spacer(1, 22))

    story.append(Paragraph(
        "Personalized Recommendations",
        styles["Heading2"]
    ))

    for recommendation in recommendations:
        story.append(Paragraph(
            f"&bull; {escape(recommendation)}",
            styles["Normal"]
        ))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "This questionnaire is an educational lifestyle demonstration. "
        "It does not provide medical advice, diagnosis or treatment.",
        styles["Italic"]
    ))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# 5. HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🌿 LifeBalance</h1>
    <p>Understand your habits. Discover your balance.</p>
    <p>
        Complete this lifestyle questionnaire to explore your
        daily habits and receive personalized educational feedback.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("YOUR LIFESTYLE. YOUR BALANCE. YOUR JOURNEY.")


# ==========================================
# 6. USER INFORMATION
# ==========================================

st.subheader("Welcome!")

name = st.text_input(
    "What is your name?",
    placeholder="Enter your name"
)

st.divider()


# ==========================================
# 7. QUESTIONNAIRE AND PROGRESS
# ==========================================

total_questions = 20

answered = sum(
    1
    for i in range(total_questions)
    if st.session_state.get(f"answer_{i}") is not None
)

progress = answered / total_questions

st.subheader("Your Assessment Progress")

st.progress(progress)

st.caption(
    f"{answered} of {total_questions} questions completed"
)

answers = {}
question_index = 0

for category_name, questions in questionnaire.items():

    st.markdown(
        f'<div class="section-title">{category_name}</div>',
        unsafe_allow_html=True
    )

    st.caption("Please choose the answer that best describes your habits.")

    with st.container(border=True):

        for question, options in questions:

            answer = st.radio(
                question,
                options,
                index=None,
                key=f"answer_{question_index}",
                horizontal=True
            )

            answers[question] = answer
            question_index += 1

            st.divider()


# ==========================================
# 8. SUBMISSION
# ==========================================

if st.button(
    "Calculate My Lifestyle Score",
    use_container_width=True
):

    if not name.strip():
        st.warning("Please enter your name.")

    elif answered != total_questions:
        st.warning(
            f"Please answer all questions. "
            f"You have completed {answered} of {total_questions}."
        )

    else:

        # ==================================
        # 9. SCORING
        # ==================================

        question_index = 0
        category_scores = {}
        recommendations = []

        for category_name, questions in questionnaire.items():

            category_total = 0

            for question, options in questions:

                selected_answer = answers[question]

                # The first option receives 1 point.
                # The last option receives 5 points.
                answer_score = options.index(selected_answer) + 1

                category_total += answer_score

                question_index += 1

            category_scores[category_name] = category_total

        total_score = sum(category_scores.values())

        # Maximum score = 100
        # Each category maximum = 20

        if total_score <= 40:
            category = "Needs Improvement"
        elif total_score <= 70:
            category = "Moderate"
        else:
            category = "Positive"


        # ==================================
        # 10. RECOMMENDATIONS
        # ==================================

        recommendation_text = {
            "Physical Activity":
                "Consider introducing regular movement and "
                "gradually building a consistent activity routine.",

            "Sleep & Recovery":
                "Consider creating a consistent sleep schedule "
                "and allowing enough time for rest.",

            "Nutrition":
                "Consider building balanced meals and including "
                "a variety of nutritious foods.",

            "Hydration":
                "Consider making water more accessible and "
                "building regular hydration habits.",

            "Lifestyle Habits":
                "Consider introducing regular breaks, relaxation "
                "and routines that support work-life balance."
        }

        for category_name, score in category_scores.items():

            if score <= 12:
                recommendations.append(
                    f"{category_name}: "
                    f"{recommendation_text[category_name]}"
                )

        if not recommendations:
            recommendations.append(
                "Your answers indicate positive habits across "
                "all five categories. Continue maintaining "
                "routines that work well for you."
            )


        # ==================================
        # 11. SAVE RESPONSES
        # ==================================

        current_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        response = {
            "Date": current_date,
            "Name": name.strip(),
            "Score": total_score,
            "Total Score": total_score,
            "Category": category
        }

        for category_name, score in category_scores.items():
            response[f"{category_name} Score"] = score

        for question, answer in answers.items():
            response[question] = answer

        response["Recommendations"] = " | ".join(
            recommendations
        )

        new_df = pd.DataFrame([response])

        file_name = "responses.csv"

        if os.path.exists(file_name):

            old_df = pd.read_csv(file_name)

            combined_df = pd.concat(
                [old_df, new_df],
                ignore_index=True,
                sort=False
            )

            combined_df.to_csv(
                file_name,
                index=False,
                encoding="utf-8-sig"
            )

        else:

            new_df.to_csv(
                file_name,
                index=False,
                encoding="utf-8-sig"
            )


        # ==================================
        # 12. DISPLAY RESULTS
        # ==================================

        st.divider()

        st.markdown(
            "<h2 style='color:#205B45;'>Your Personal Results</h2>",
            unsafe_allow_html=True
        )

        st.write(f"Welcome, **{name.strip()}**!")

        col1, col2 = st.columns(2)

        col1.metric(
            "Overall Lifestyle Score",
            f"{total_score}/100"
        )

        col2.metric(
            "Assessment Level",
            category
        )

        st.progress(total_score / 100)

        st.subheader("Your Category Results")

        results_df = pd.DataFrame({
            "Category": list(category_scores.keys()),
            "Score": list(category_scores.values())
        })

        st.bar_chart(
    results_df.set_index("Category"),
    y="Score"
)

        for category_name, score in category_scores.items():

            st.write(f"**{category_name}: {score}/20**")

        st.subheader("Your Personalized Recommendations")

        for recommendation in recommendations:
            st.info(recommendation)


        # ==================================
        # 13. PDF DOWNLOAD
        # ==================================

        pdf_data = create_pdf(
            name.strip(),
            current_date,
            total_score,
            category,
            category_scores,
            recommendations
        )

        st.download_button(
            label="📄 Download My Lifestyle Report",
            data=pdf_data,
            file_name="LifeBalance_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.success(
            "Your assessment has been completed and saved!"
        )

        st.caption(
            "Educational demonstration only. "
            "This questionnaire is not a medical assessment."
        )


# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.markdown(
    "<div style='text-align:center;color:#718078;'>"
    "LifeBalance © 2026 | Lifestyle Assessment Demo"
    "</div>",
    unsafe_allow_html=True
)
