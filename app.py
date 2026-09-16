import json
import html
from pathlib import Path

import streamlit as st


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="CabinCrewHub",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# FILES
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
AIRLINES_FILE = BASE_DIR / "airlines.json"


# ------------------------------------------------------------
# LOAD AIRLINE DATA
# ------------------------------------------------------------

def load_airlines():
    try:
        with open(AIRLINES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            st.error("The airline data file is not correctly formatted.")
            st.stop()

        return data

    except FileNotFoundError:
        st.error("The airline data file could not be found.")
        st.stop()

    except json.JSONDecodeError:
        st.error("The airline data file contains invalid JSON.")
        st.stop()


airlines = load_airlines()


def safe(value):
    return html.escape(str(value))


# ------------------------------------------------------------
# STYLING
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f6f8;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e5e9;
    }

    .brand {
        padding: 8px 0 24px 0;
    }

    .brand-name {
        font-size: 24px;
        font-weight: 700;
        color: #172033;
        margin: 0;
    }

    .brand-subtitle {
        color: #737b88;
        font-size: 13px;
        margin-top: 5px;
    }

    .page-header {
        background: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 28px 30px;
        margin-bottom: 24px;
    }

    .page-header h1 {
        margin: 0;
        color: #172033;
        font-size: 30px;
        font-weight: 700;
    }

    .page-header p {
        margin: 8px 0 0 0;
        color: #697281;
        font-size: 15px;
    }

    .section {
        background: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .section-title {
        color: #172033;
        font-size: 20px;
        font-weight: 650;
        margin-bottom: 5px;
    }

    .section-description {
        color: #697281;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .airline-title {
        color: #172033;
        font-size: 22px;
        font-weight: 650;
        margin: 0;
    }

    .airline-description {
        color: #697281;
        font-size: 14px;
        margin-top: 7px;
    }

    .result-summary {
        background: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 24px;
        margin: 20px 0;
    }

    .result-label {
        color: #697281;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .result-score {
        color: #172033;
        font-size: 38px;
        font-weight: 700;
        margin: 4px 0;
    }

    .result-text {
        color: #697281;
        font-size: 14px;
    }

    .requirement {
        background: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 8px;
    }

    .requirement-pass {
        border-left: 4px solid #27864b;
    }

    .requirement-fail {
        border-left: 4px solid #c63c3c;
    }

    .requirement-title {
        color: #202735;
        font-size: 14px;
        font-weight: 600;
    }

    .requirement-detail {
        color: #737b88;
        font-size: 13px;
        margin-top: 4px;
    }

    .footer {
        text-align: center;
        color: #8a919c;
        font-size: 12px;
        padding-top: 25px;
    }

    div[data-testid="stButton"] button {
        border-radius: 6px;
        min-height: 42px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-name">CabinCrewHub</div>
        <div class="brand-subtitle">
            Cabin crew recruitment tools
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Menu",
    [
        "Airline Checker",
        "Interview Trainer",
    ],
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "For applicant preparation and reference."
)


# ============================================================
# AIRLINE CHECKER
# ============================================================

if page == "Airline Checker":

    st.markdown(
        """
        <div class="page-header">
            <h1>Airline Application Checker</h1>
            <p>
                Compare your profile with the recruitment criteria
                stored for each airline.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # AIRLINE
    # --------------------------------------------------------

    airline_names = list(airlines.keys())

    if not airline_names:
        st.error("No airlines are available.")
        st.stop()

    airline = st.selectbox(
        "Airline",
        airline_names,
    )

    airline_data = airlines[airline]

    description = airline_data.get(
        "description",
        f"Cabin crew recruitment requirements for {airline}."
    )


    st.markdown(
        f"""
        <div class="section">

            <div class="airline-title">
                {safe(airline)}
            </div>

            <div class="airline-description">
                {safe(description)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section">

            <div class="section-title">
                Applicant Information
            </div>

            <div class="section-description">
                Enter your current information below.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        age = st.number_input(
            "Age",
            min_value=16,
            max_value=70,
            value=19,
            step=1,
        )

        height = st.number_input(
            "Height (cm)",
            min_value=130,
            max_value=220,
            value=171,
            step=1,
        )

        reach = st.number_input(
            "Arm reach (cm)",
            min_value=150,
            max_value=250,
            value=220,
            step=1,
        )

        experience = st.number_input(
            "Customer service / hospitality experience (years)",
            min_value=0.0,
            max_value=50.0,
            value=3.0,
            step=0.5,
        )


    with col2:

        english = st.selectbox(
            "English proficiency",
            [
                "Very Fluent",
                "Fluent",
                "Intermediate",
                "Basic",
                "Not fluent",
            ],
        )

        education = st.selectbox(
            "Secondary education",
            [
                "Meets requirement",
                "Does not meet requirement",
            ],
        )

        swimming = st.selectbox(
            "Swimming",
            [
                "Yes",
                "No",
            ],
        )

        tattoos = st.selectbox(
            "Visible tattoos",
            [
                "No",
                "Yes",
            ],
        )


    st.markdown("")


    check = st.button(
        "Check Requirements",
        type="primary",
        use_container_width=True,
    )


    # --------------------------------------------------------
    # CHECK REQUIREMENTS
    # --------------------------------------------------------

    if check:

        results = []


        # AGE
        min_age = airline_data.get("min_age")

        if min_age and min_age > 0:

            results.append(
                {
                    "name": "Age",
                    "passed": age >= min_age,
                    "detail": (
                        f"Your age: {age}. "
                        f"Minimum: {min_age}."
                    ),
                }
            )


        # HEIGHT
        min_height = airline_data.get("min_height")

        if min_height and min_height > 0:

            results.append(
                {
                    "name": "Height",
                    "passed": height >= min_height,
                    "detail": (
                        f"Your height: {height} cm. "
                        f"Minimum: {min_height} cm."
                    ),
                }
            )


        # REACH
        min_reach = airline_data.get("min_reach")

        if min_reach and min_reach > 0:

            results.append(
                {
                    "name": "Arm reach",
                    "passed": reach >= min_reach,
                    "detail": (
                        f"Your reach: {reach} cm. "
                        f"Minimum: {min_reach} cm."
                    ),
                }
            )


        # ENGLISH
        english_required = airline_data.get(
            "english_required",
            False
        )

        if english_required:

            passed = english in [
                "Very Fluent",
                "Fluent",
            ]

            results.append(
                {
                    "name": "English proficiency",
                    "passed": passed,
                    "detail": (
                        f"Your level: {english}. "
                        "Fluent English is required."
                    ),
                }
            )


        # EDUCATION
        education_required = airline_data.get(
            "secondary_education_required",
            False
        )

        if education_required:

            passed = (
                education == "Meets requirement"
            )

            results.append(
                {
                    "name": "Secondary education",
                    "passed": passed,
                    "detail": (
                        "Requirement met."
                        if passed
                        else
                        "Requirement not met."
                    ),
                }
            )


        # EXPERIENCE
        experience_required = airline_data.get(
            "experience_required",
            False
        )

        minimum_experience = airline_data.get(
            "minimum_experience_years",
            0
        )

        if experience_required:

            passed = (
                experience >= minimum_experience
            )

            results.append(
                {
                    "name": "Experience",
                    "passed": passed,
                    "detail": (
                        f"Your experience: "
                        f"{experience:g} years. "
                        f"Minimum: "
                        f"{minimum_experience:g} years."
                    ),
                }
            )


        # SWIMMING
        swimming_required = airline_data.get(
            "swimming_required",
            False
        )

        if swimming_required:

            passed = swimming == "Yes"

            results.append(
                {
                    "name": "Swimming",
                    "passed": passed,
                    "detail": (
                        "Requirement met."
                        if passed
                        else
                        "Requirement not met."
                    ),
                }
            )


        # TATTOOS
        no_visible_tattoos = airline_data.get(
            "no_visible_tattoos",
            False
        )

        if no_visible_tattoos:

            passed = tattoos == "No"

            results.append(
                {
                    "name": "Visible tattoos",
                    "passed": passed,
                    "detail": (
                        "No visible tattoos reported."
                        if passed
                        else
                        "Visible tattoos reported."
                    ),
                }
            )


        # ----------------------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------------------

        if results:

            passed_count = sum(
                result["passed"]
                for result in results
            )

            total_count = len(results)

            percentage = round(
                (passed_count / total_count) * 100
            )


            st.markdown(
                f"""
                <div class="result-summary">

                    <div class="result-label">
                        Requirements checked
                    </div>

                    <div class="result-score">
                        {percentage}%
                    </div>

                    <div class="result-text">
                        {passed_count} of {total_count}
                        stored requirements met.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


            st.progress(
                percentage / 100
            )


            st.subheader(
                "Requirement Details"
            )


            for result in results:

                if result["passed"]:

                    st.markdown(
                        f"""
                        <div class="requirement requirement-pass">

                            <div class="requirement-title">
                                {safe(result["name"])} — Met
                            </div>

                            <div class="requirement-detail">
                                {safe(result["detail"])}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="requirement requirement-fail">

                            <div class="requirement-title">
                                {safe(result["name"])} — Not Met
                            </div>

                            <div class="requirement-detail">
                                {safe(result["detail"])}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


            st.caption(
                "The results are based on the requirements stored "
                "in the application's airline data."
            )


        else:

            st.warning(
                "No requirements have been configured for this airline."
            )


# ============================================================
# INTERVIEW TRAINER
# ============================================================

elif page == "Interview Trainer":

    st.markdown(
        """
        <div class="page-header">

            <h1>Interview Trainer</h1>

            <p>
                Practice common cabin crew interview questions.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    questions = [

        {
            "category": "Introduction",
            "question": "Tell me about yourself.",
        },

        {
            "category": "Motivation",
            "question": "Why do you want to become cabin crew?",
        },

        {
            "category": "Motivation",
            "question": "Why do you want to work for this airline?",
        },

        {
            "category": "Customer Service",
            "question": "Tell me about a time you dealt with a difficult customer.",
        },

        {
            "category": "Customer Service",
            "question": "How would you handle an angry passenger?",
        },

        {
            "category": "Teamwork",
            "question": "Tell me about a time you worked as part of a team.",
        },

        {
            "category": "Teamwork",
            "question": "How would you handle a disagreement with another crew member?",
        },

        {
            "category": "Safety",
            "question": "What would you do if a passenger refused to follow a safety instruction?",
        },

        {
            "category": "Cabin Crew",
            "question": "What are the main responsibilities of cabin crew?",
        },

        {
            "category": "Customer Service",
            "question": "What does excellent customer service mean to you?",
        },

        {
            "category": "General",
            "question": "Why should we hire you?",
        },

    ]


    categories = sorted(
        set(
            question["category"]
            for question in questions
        )
    )


    selected_category = st.selectbox(
        "Category",
        ["All"] + categories,
    )


    if selected_category == "All":

        filtered_questions = questions

    else:

        filtered_questions = [
            question
            for question in questions
            if question["category"] == selected_category
        ]


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    question_number = st.number_input(
        "Question number",
        min_value=1,
        max_value=len(filtered_questions),
        value=1,
        step=1,
    )


    current_question = filtered_questions[
        question_number - 1
    ]


    st.markdown(
        f"""
        <div class="section">

            <div class="section-description">
                {safe(current_question["category"])}
            </div>

            <div class="section-title">
                {safe(current_question["question"])}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    answer = st.text_area(
        "Your answer",
        height=220,
        placeholder="Write your answer here.",
    )


    col1, col2 = st.columns(2)


    with col1:

        show_tips = st.button(
            "Interview Tips",
            use_container_width=True,
        )


    with col2:

        check_answer = st.button(
            "Review Answer",
            use_container_width=True,
        )


    # --------------------------------------------------------
    # INTERVIEW TIPS
    # --------------------------------------------------------

    if show_tips:

        st.markdown(
            """
            ### Answer structure

            For questions about previous experiences, use the STAR
            structure:

            **Situation**  
            Explain the situation briefly.

            **Task**  
            Explain what you were responsible for.

            **Action**  
            Explain what you did.

            **Result**  
            Explain the outcome.

            Keep your answer specific and relevant to the question.
            """,
        )


    # --------------------------------------------------------
    # ANSWER REVIEW
    # --------------------------------------------------------

    if check_answer:

        if not answer.strip():

            st.warning(
                "Enter an answer before reviewing it."
            )

        else:

            words = answer.strip().split()
            word_count = len(words)


            st.subheader(
                "Answer Review"
            )


            if word_count < 30:

                st.warning(
                    "The answer is quite short. "
                    "Consider adding a specific example."
                )

            elif word_count <= 120:

                st.success(
                    "The answer is an appropriate length. "
                    "Check that it directly answers the question."
                )

            else:

                st.info(
                    "The answer is detailed. "
                    "Consider removing information that is not directly relevant."
                )


            lower_answer = answer.lower()


            keywords = [
                "customer",
                "passenger",
                "team",
                "safety",
                "communication",
                "service",
                "problem",
                "professional",
            ]


            found_keywords = [
                word
                for word in keywords
                if word in lower_answer
            ]


            if found_keywords:

                st.write(
                    "Relevant terms used: "
                    + ", ".join(found_keywords)
                    + "."
                )

            else:

                st.write(
                    "Consider including relevant examples "
                    "from your customer service, teamwork, "
                    "communication or problem-solving experience "
                    "when appropriate."
                )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        CabinCrewHub
    </div>
    """,
    unsafe_allow_html=True,
)
