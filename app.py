import json
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CabinCrewHub",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# AIRLINE DATA FILE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
AIRLINES_FILE = BASE_DIR / "airlines.json"


# ============================================================
# LOAD AIRLINE DATA
# ============================================================

def load_airlines():
    try:
        with open(AIRLINES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            st.error("The airline data is not correctly formatted.")
            st.stop()

        return data

    except FileNotFoundError:
        st.error(
            "airlines.json could not be found. "
            "Make sure it is in the same folder as app.py."
        )
        st.stop()

    except json.JSONDecodeError as error:
        st.error(
            f"airlines.json contains invalid JSON: {error}"
        )
        st.stop()


airlines = load_airlines()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("CabinCrewHub")

st.sidebar.caption(
    "Cabin crew recruitment tools"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Menu",
    [
        "Airline Checker",
        "Interview Trainer",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "For applicant preparation and reference."
)


# ============================================================
# AIRLINE APPLICATION CHECKER
# ============================================================

if page == "Airline Checker":

    st.title("Airline Application Checker")

    st.write(
        "Compare your profile with the recruitment criteria "
        "stored for the selected airline."
    )

    st.divider()

    # --------------------------------------------------------
    # AIRLINE SELECTION
    # --------------------------------------------------------

    airline_names = list(airlines.keys())

    if not airline_names:
        st.error("No airlines have been added yet.")
        st.stop()

    airline = st.selectbox(
        "Select an airline",
        airline_names,
    )

    airline_data = airlines[airline]

    description = airline_data.get(
        "description",
        f"Cabin crew recruitment requirements for {airline}."
    )

    st.subheader(airline)

    st.write(description)

    st.divider()

    # --------------------------------------------------------
    # APPLICANT INFORMATION
    # --------------------------------------------------------

    st.subheader("Applicant Information")

    st.write(
        "Enter your current information below."
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

    st.write("")

    check_profile = st.button(
        "Check Requirements",
        type="primary",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # CHECK PROFILE
    # --------------------------------------------------------

    if check_profile:

        results = []

        # ====================================================
        # AGE
        # ====================================================

        min_age = airline_data.get("min_age")

        if min_age and min_age > 0:

            passed = age >= min_age

            results.append(
                {
                    "name": "Age",
                    "passed": passed,
                    "detail": (
                        f"Your age: {age}. "
                        f"Minimum required: {min_age}."
                    ),
                }
            )

        # ====================================================
        # HEIGHT
        # ====================================================

        min_height = airline_data.get("min_height")

        if min_height and min_height > 0:

            passed = height >= min_height

            results.append(
                {
                    "name": "Height",
                    "passed": passed,
                    "detail": (
                        f"Your height: {height} cm. "
                        f"Minimum required: {min_height} cm."
                    ),
                }
            )

        # ====================================================
        # ARM REACH
        # ====================================================

        min_reach = airline_data.get("min_reach")

        if min_reach and min_reach > 0:

            passed = reach >= min_reach

            results.append(
                {
                    "name": "Arm reach",
                    "passed": passed,
                    "detail": (
                        f"Your reach: {reach} cm. "
                        f"Minimum required: {min_reach} cm."
                    ),
                }
            )

        # ====================================================
        # ENGLISH
        # ====================================================

        english_required = airline_data.get(
            "english_required",
            False,
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

        # ====================================================
        # SECONDARY EDUCATION
        # ====================================================

        education_required = airline_data.get(
            "secondary_education_required",
            False,
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
                        "The education requirement is marked "
                        "as met."
                        if passed
                        else
                        "The education requirement is marked "
                        "as not met."
                    ),
                }
            )

        # ====================================================
        # EXPERIENCE
        # ====================================================

        experience_required = airline_data.get(
            "experience_required",
            False,
        )

        minimum_experience = airline_data.get(
            "minimum_experience_years",
            0,
        )

        if experience_required:

            passed = (
                experience >= minimum_experience
            )

            results.append(
                {
                    "name": "Customer service / hospitality experience",
                    "passed": passed,
                    "detail": (
                        f"Your experience: {experience:g} years. "
                        f"Minimum required: "
                        f"{minimum_experience:g} years."
                    ),
                }
            )

        # ====================================================
        # SWIMMING
        # ====================================================

        swimming_required = airline_data.get(
            "swimming_required",
            False,
        )

        if swimming_required:

            passed = swimming == "Yes"

            results.append(
                {
                    "name": "Swimming",
                    "passed": passed,
                    "detail": (
                        "Swimming requirement met."
                        if passed
                        else
                        "Swimming requirement not met."
                    ),
                }
            )

        # ====================================================
        # VISIBLE TATTOOS
        # ====================================================

        no_visible_tattoos = airline_data.get(
            "no_visible_tattoos",
            False,
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

        # ====================================================
        # RESULTS
        # ====================================================

        st.divider()

        if results:

            passed_count = sum(
                1
                for result in results
                if result["passed"]
            )

            total_count = len(results)

            percentage = round(
                (passed_count / total_count) * 100
            )

            st.subheader("Results")

            st.metric(
                "Requirements met",
                f"{passed_count} of {total_count}",
            )

            st.progress(
                percentage / 100
            )

            st.write(
                f"{percentage}% of the stored requirements "
                f"are currently met."
            )

            st.divider()

            st.subheader("Requirement Details")

            for result in results:

                if result["passed"]:

                    st.success(
                        f"{result['name']}: Met"
                    )

                    st.caption(
                        result["detail"]
                    )

                else:

                    st.error(
                        f"{result['name']}: Not Met"
                    )

                    st.caption(
                        result["detail"]
                    )

            st.divider()

            st.caption(
                "This tool compares your information with "
                "the requirements stored in airlines.json. "
                "It is not an official airline recruitment decision."
            )

        else:

            st.warning(
                "No requirements have been configured "
                "for this airline."
            )


# ============================================================
# INTERVIEW TRAINER
# ============================================================

elif page == "Interview Trainer":

    st.title("Interview Trainer")

    st.write(
        "Practice common cabin crew interview questions."
    )

    st.divider()

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

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

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
    # QUESTION SELECTION
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

    st.subheader(
        current_question["question"]
    )

    st.caption(
        current_question["category"]
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

        review_answer = st.button(
            "Review Answer",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # INTERVIEW TIPS
    # --------------------------------------------------------

    if show_tips:

        st.info(
            """
            For questions about previous experiences, use the
            STAR structure.

            Situation:
            Explain the situation briefly.

            Task:
            Explain what you were responsible for.

            Action:
            Explain what you did.

            Result:
            Explain the outcome.

            Keep the answer specific and relevant to the question.
            """
        )

    # --------------------------------------------------------
    # ANSWER REVIEW
    # --------------------------------------------------------

    if review_answer:

        if not answer.strip():

            st.warning(
                "Enter an answer before reviewing it."
            )

        else:

            words = answer.strip().split()

            word_count = len(words)

            st.subheader("Answer Review")

            st.write(
                f"Word count: {word_count}"
            )

            if word_count < 30:

                st.warning(
                    "The answer is quite short. "
                    "Consider adding a specific example."
                )

            elif word_count <= 120:

                st.success(
                    "The answer is an appropriate length. "
                    "Make sure it directly answers the question."
                )

            else:

                st.info(
                    "The answer is detailed. "
                    "Consider removing information that is "
                    "not directly relevant."
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
                    "Consider using a specific example "
                    "related to customer service, teamwork, "
                    "communication, safety or problem solving "
                    "when relevant to the question."
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption("CabinCrewHub")
