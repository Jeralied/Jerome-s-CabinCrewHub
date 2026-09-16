import streamlit as st
import json
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CabinCrewHub",
    page_icon="✈️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.hero {
    padding: 40px;
    border-radius: 20px;
    background: linear-gradient(135deg, #081b33, #174b78);
    color: white;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 44px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

.card {
    padding: 25px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e9f0;
    margin-bottom: 20px;
}

.result-box {
    padding: 18px;
    border-radius: 12px;
    margin: 10px 0;
    background: #ffffff;
    border: 1px solid #e2e8f0;
}

.check {
    font-size: 19px;
    font-weight: 600;
}

.small-text {
    color: #64748b;
    font-size: 14px;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD AIRLINE DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
AIRLINE_FILE = BASE_DIR / "airlines.json"


def load_airlines():

    try:

        with open(AIRLINE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:

        st.error(
            "airlines.json was not found. "
            "Make sure the file is in the same GitHub repository."
        )

        return {}

    except json.JSONDecodeError:

        st.error(
            "airlines.json contains invalid JSON."
        )

        return {}


airlines = load_airlines()

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <h1>✈️ CabinCrewHub</h1>

    <p>
        Your cabin crew preparation and airline application companion.
    </p>

</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("✈️ CabinCrewHub")

page = st.sidebar.radio(
    "Choose a tool",
    [
        "🔎 Airline Checker",
        "🎤 Interview Trainer"
    ]
)

# ============================================================
# AIRLINE CHECKER
# ============================================================

if page == "🔎 Airline Checker":

    st.subheader("🔎 Airline Application Checker")

    st.write(
        "Enter your information to compare your profile "
        "with the requirements currently stored for the selected airline."
    )

    if not airlines:

        st.warning("No airline information is available.")

        st.stop()

    # --------------------------------------------------------
    # SELECT AIRLINE
    # --------------------------------------------------------

    selected_airline = st.selectbox(
        "Select an airline",
        list(airlines.keys())
    )

    airline = airlines[selected_airline]

    st.markdown(
        f"""
        <div class="card">

            <h2>✈️ {selected_airline}</h2>

            <p>
                {airline.get("description", "")}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # USER PROFILE
    # --------------------------------------------------------

    st.subheader("👤 Your Profile")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=16,
            max_value=70,
            value=19
        )

        height = st.number_input(
            "Height (cm)",
            min_value=140,
            max_value=220,
            value=171
        )

        reach = st.number_input(
            "Arm Reach (cm)",
            min_value=150,
            max_value=250,
            value=220
        )

    with col2:

        english = st.selectbox(
            "English ability",
            [
                "Fluent",
                "Good",
                "Basic",
                "None"
            ]
        )

        education = st.selectbox(
            "Highest education",
            [
                "Below secondary school",
                "Secondary school / Grade 12",
                "Diploma",
                "Bachelor's degree",
                "Master's degree"
            ]
        )

        experience = st.number_input(
            "Customer service / hospitality experience (years)",
            min_value=0.0,
            max_value=30.0,
            value=3.0,
            step=0.5
        )

    swimming = st.selectbox(
        "Can you swim?",
        [
            "Yes",
            "No",
            "Not sure"
        ]
    )

    tattoos = st.selectbox(
        "Visible tattoos while wearing the airline uniform?",
        [
            "No",
            "Yes",
            "Not sure"
        ]
    )

    st.divider()

    # --------------------------------------------------------
    # CHECK BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔍 Check My Requirements",
        type="primary",
        use_container_width=True
    ):

        results = []

        # ====================================================
        # AGE
        # ====================================================

        if "min_age" in airline:

            if age >= airline["min_age"]:

                results.append(
                    (
                        "✓",
                        "Age",
                        f"You meet the minimum age of "
                        f"{airline['min_age']}.",
                        "success"
                    )
                )

            else:

                results.append(
                    (
                        "✗",
                        "Age",
                        f"Minimum age: {airline['min_age']}.",
                        "error"
                    )
                )

        # ====================================================
        # HEIGHT
        # ====================================================

        if "min_height" in airline:

            if airline["min_height"] > 0:

                if height >= airline["min_height"]:

                    results.append(
                        (
                            "✓",
                            "Height",
                            f"You meet the minimum height of "
                            f"{airline['min_height']} cm.",
                            "success"
                        )
                    )

                else:

                    results.append(
                        (
                            "✗",
                            "Height",
                            f"Minimum height: "
                            f"{airline['min_height']} cm.",
                            "error"
                        )
                    )

            else:

                results.append(
                    (
                        "⚠",
                        "Height",
                        "No height requirement stored. "
                        "Verify the current airline vacancy.",
                        "warning"
                    )
                )

        # ====================================================
        # ARM REACH
        # ====================================================

        if "min_reach" in airline:

            if airline["min_reach"] > 0:

                if reach >= airline["min_reach"]:

                    results.append(
                        (
                            "✓",
                            "Arm Reach",
                            f"You meet the minimum reach of "
                            f"{airline['min_reach']} cm.",
                            "success"
                        )
                    )

                else:

                    results.append(
                        (
                            "✗",
                            "Arm Reach",
                            f"Minimum reach: "
                            f"{airline['min_reach']} cm.",
                            "error"
                        )
                    )

            else:

                results.append(
                    (
                        "⚠",
                        "Arm Reach",
                        "No arm-reach requirement stored. "
                        "Verify the current airline vacancy.",
                        "warning"
                    )
                )

        # ====================================================
        # ENGLISH
        # ====================================================

        if airline.get("english_required", False):

            if english == "Fluent":

                results.append(
                    (
                        "✓",
                        "English",
                        "Fluent English selected.",
                        "success"
                    )
                )

            else:

                results.append(
                    (
                        "⚠",
                        "English",
                        "The airline requires English proficiency. "
                        "Verify that your level meets the vacancy requirement.",
                        "warning"
                    )
                )

        # ====================================================
        # EDUCATION
        # ====================================================

        if airline.get(
            "secondary_education_required",
            False
        ):

            valid_education = [
                "Secondary school / Grade 12",
                "Diploma",
                "Bachelor's degree",
                "Master's degree"
            ]

            if education in valid_education:

                results.append(
                    (
                        "✓",
                        "Education",
                        "Secondary education or higher selected.",
                        "success"
                    )
                )

            else:

                results.append(
                    (
                        "✗",
                        "Education",
                        "Secondary education is required.",
                        "error"
                    )
                )

        # ====================================================
        # EXPERIENCE
        # ====================================================

        if airline.get(
            "experience_required",
            False
        ):

            required_experience = airline.get(
                "minimum_experience_years",
                1
            )

            if experience >= required_experience:

                results.append(
                    (
                        "✓",
                        "Experience",
                        f"You entered {experience:g} year(s) "
                        f"of relevant experience.",
                        "success"
                    )
                )

            else:

                results.append(
                    (
                        "✗",
                        "Experience",
                        f"At least {required_experience} "
                        f"year(s) required.",
                        "error"
                    )
                )

        else:

            results.append(
                (
                    "⚠",
                    "Experience",
                    "No minimum experience requirement "
                    "is stored for this airline.",
                    "warning"
                )
            )

        # ====================================================
        # SWIMMING
        # ====================================================

        if airline.get(
            "swimming_required",
            False
        ):

            if swimming == "Yes":

                results.append(
                    (
                        "✓",
                        "Swimming",
                        "Swimming ability confirmed.",
                        "success"
                    )
                )

            elif swimming == "No":

                results.append(
                    (
                        "✗",
                        "Swimming",
                        "Swimming requirement not met.",
                        "error"
                    )
                )

            else:

                results.append(
                    (
                        "⚠",
                        "Swimming",
                        "Verify the airline's swimming requirement.",
                        "warning"
                    )
                )

        # ====================================================
        # VISIBLE TATTOOS
        # ====================================================

        if airline.get(
            "no_visible_tattoos",
            False
        ):

            if tattoos == "No":

                results.append(
                    (
                        "✓",
                        "Visible Tattoos",
                        "No visible tattoos selected.",
                        "success"
                    )
                )

            elif tattoos == "Yes":

                results.append(
                    (
                        "✗",
                        "Visible Tattoos",
                        "Visible tattoos may conflict with "
                        "the airline's stated requirement.",
                        "error"
                    )
                )

            else:

                results.append(
                    (
                        "⚠",
                        "Visible Tattoos",
                        "Verify the airline's current "
                        "uniform/tattoo policy.",
                        "warning"
                    )
                )

        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        st.subheader("📋 Requirement Results")

        for icon, requirement, message, status in results:

            st.markdown(
                f"""
                <div class="result-box">

                    <div class="check">
                        {icon} {requirement}
                    </div>

                    <div class="small-text">
                        {message}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # ====================================================
        # SUMMARY
        # ====================================================

        passed = sum(
            1 for result in results
            if result[3] == "success"
        )

        failed = sum(
            1 for result in results
            if result[3] == "error"
        )

        warnings = sum(
            1 for result in results
            if result[3] == "warning"
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "✓ Meets",
                passed
            )

        with col2:
            st.metric(
                "⚠ Verify",
                warnings
            )

        with col3:
            st.metric(
                "✗ Does Not Meet",
                failed
            )

        if failed == 0:

            st.success(
                "No stored requirement was marked as not met. "
                "Review all verification warnings and the airline's "
                "official vacancy before applying."
            )

        else:

            st.error(
                "At least one stored requirement was not met."
            )

        st.info(
            "Important: This is a requirement checklist, not an "
            "employment or selection prediction. Airline requirements "
            "can change, so applicants should verify the current "
            "official vacancy."
        )


# ============================================================
# INTERVIEW TRAINER
# ============================================================

elif page == "🎤 Interview Trainer":

    st.subheader("🎤 Cabin Crew Interview Trainer")

    st.write(
        "Practice realistic cabin crew interview questions and "
        "receive structured feedback on your answer."
    )

    # -----------------------------
    # LOAD QUESTIONS
    # -----------------------------

    QUESTION_FILE = BASE_DIR / "questions.json"

    try:
        with open(QUESTION_FILE, "r", encoding="utf-8") as file:
            questions = json.load(file)
    except FileNotFoundError:
        st.error("questions.json was not found.")
        st.stop()
    except json.JSONDecodeError:
        st.error("questions.json contains invalid JSON.")
        st.stop()

    # -----------------------------
    # SESSION STATE
    # -----------------------------

    if "interview_question" not in st.session_state:
        st.session_state.interview_question = None

    if "interview_score" not in st.session_state:
        st.session_state.interview_score = None

    if "interview_feedback" not in st.session_state:
        st.session_state.interview_feedback = None

    if "interview_category" not in st.session_state:
        st.session_state.interview_category = "All"

    # -----------------------------
    # CATEGORY
    # -----------------------------

    categories = ["All"] + sorted(
        list(set(q["category"] for q in questions))
    )

    selected_category = st.selectbox(
        "Choose interview category",
        categories
    )

    # -----------------------------
    # NEW QUESTION
    # -----------------------------

    if st.session_state.interview_question is None:

        available_questions = questions

        if selected_category != "All":
            available_questions = [
                q for q in questions
                if q["category"] == selected_category
            ]

        st.session_state.interview_question = random.choice(
            available_questions
        )

        st.session_state.interview_category = selected_category

    question = st.session_state.interview_question

    # -----------------------------
    # QUESTION CARD
    # -----------------------------

    st.markdown(
        f"""
        <div class="card">
            <p class="small-text">{question["category"]}</p>
            <h2>{question["question"]}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------
    # ANSWER
    # -----------------------------

    answer = st.text_area(
        "Your answer",
        placeholder=(
            "Type your interview answer here...\n\n"
            "Tip: Use a real example when possible."
        ),
        height=220,
        key=f"answer_{id(question)}"
    )

    # -----------------------------
    # STAR GUIDE
    # -----------------------------

    with st.expander("⭐ Need help structuring your answer?"):

        st.markdown("""
        **S — Situation**  
        What was happening?

        **T — Task**  
        What responsibility did you have?

        **A — Action**  
        What did YOU do?

        **R — Result**  
        What happened because of your actions?
        """)

    # -----------------------------
    # EVALUATE ANSWER
    # -----------------------------

    if st.button(
        "🎯 Evaluate My Answer",
        type="primary",
        use_container_width=True
    ):

        if not answer.strip():

            st.warning("Please write an answer before evaluating it.")

        else:

            text = answer.strip()
            words = text.split()
            word_count = len(words)
            lower = text.lower()

            score = 1
            feedback = []
            strengths = []
            improvements = []

            # LENGTH
            if 40 <= word_count <= 180:
                score += 1
                strengths.append(
                    "Your answer has a suitable amount of detail."
                )
            elif word_count < 40:
                improvements.append(
                    "Your answer is quite short. Add more detail or a specific example."
                )
            else:
                improvements.append(
                    "Your answer may be longer than necessary. Keep it focused."
                )

            # CUSTOMER SERVICE
            service_words = [
                "customer",
                "passenger",
                "guest",
                "service",
                "help",
                "assist",
                "support",
                "satisfied"
            ]

            if any(word in lower for word in service_words):
                score += 1
                strengths.append(
                    "You demonstrated customer-service awareness."
                )
            else:
                improvements.append(
                    "Connect your answer more clearly to customer service."
                )

            # COMMUNICATION
            communication_words = [
                "listen",
                "communicate",
                "explain",
                "understand",
                "conversation",
                "calm",
                "respect"
            ]

            if any(word in lower for word in communication_words):
                strengths.append(
                    "You showed useful communication or interpersonal skills."
                )
            else:
                improvements.append(
                    "Mention how you communicated with the people involved."
                )

            # TEAMWORK
            teamwork_words = [
                "team",
                "colleague",
                "together",
                "cooperate",
                "support",
                "collaborate"
            ]

            if any(word in lower for word in teamwork_words):
                strengths.append(
                    "Your answer demonstrates teamwork awareness."
                )
            else:
                improvements.append(
                    "Where relevant, explain how you worked with others."
                )

            # STAR SIGNALS
            star_words = [
                "situation",
                "task",
                "action",
                "result",
                "because",
                "therefore",
                "eventually"
            ]

            star_count = sum(
                1 for word in star_words
                if word in lower
            )

            if star_count >= 3:
                score += 1
                strengths.append(
                    "Your answer contains several elements of a structured example."
                )
            else:
                improvements.append(
                    "Use a clear Situation → Task → Action → Result structure when appropriate."
                )

            # CAP SCORE
            score = min(score, 5)

            # EXTRA FEEDBACK
            if "I" in answer or "my" in lower:
                strengths.append(
                    "You focused on your own actions rather than only describing the situation."
                )
            else:
                improvements.append(
                    "Be specific about what YOU personally did."
                )

            if score >= 4:
                overall = "Strong answer"
            elif score == 3:
                overall = "Good foundation"
            else:
                overall = "Needs improvement"

            st.session_state.interview_score = score

            st.session_state.interview_feedback = {
                "overall": overall,
                "strengths": strengths,
                "improvements": improvements,
                "word_count": word_count
            }

    # -----------------------------
    # FEEDBACK
    # -----------------------------

    if st.session_state.interview_feedback is not None:

        feedback = st.session_state.interview_feedback

        st.divider()

        st.subheader("📊 Your Feedback")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Score",
                f"{st.session_state.interview_score}/5"
            )

        with col2:
            st.metric(
                "Words",
                feedback["word_count"]
            )

        st.markdown(
            f"### {feedback['overall']}"
        )

        if feedback["strengths"]:

            st.markdown("#### ✅ Strengths")

            for item in feedback["strengths"]:
                st.write(f"✓ {item}")

        if feedback["improvements"]:

            st.markdown("#### 🛠️ Improve")

            for item in feedback["improvements"]:
                st.write(f"• {item}")

        st.info(
            f"💡 Interview tip: {question['tip']}"
        )

        # -----------------------------
        # NEXT QUESTION
        # -----------------------------

        if st.button(
            "➡️ Next Question",
            use_container_width=True
        ):

            available_questions = questions

            if st.session_state.interview_category != "All":
                available_questions = [
                    q for q in questions
                    if q["category"] ==
                    st.session_state.interview_category
                ]

            current_question = st.session_state.interview_question

            other_questions = [
                q for q in available_questions
                if q != current_question
            ]

            if other_questions:
                st.session_state.interview_question = random.choice(
                    other_questions
                )
            else:
                st.session_state.interview_question = random.choice(
                    available_questions
                )

            st.session_state.interview_score = None
            st.session_state.interview_feedback = None

            st.rerun()
