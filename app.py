import json
import html
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CabinCrewHub",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
AIRLINES_FILE = BASE_DIR / "airlines.json"
QUESTIONS_FILE = BASE_DIR / "questions.json"


# ============================================================
# LOAD JSON SAFELY
# ============================================================

def load_json(path, default):
    """Load a JSON file safely."""
    try:
        if not path.exists():
            return default

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return default


airlines_data = load_json(AIRLINES_FILE, {})
questions_data = load_json(QUESTIONS_FILE, [])


# ============================================================
# NORMALIZE AIRLINE DATA
# ============================================================

def get_airlines(data):
    """
    Supports either:
        {"Emirates": {...}, "Qatar Airways": {...}}
    or:
        [{"name": "Emirates", ...}, ...]
    """

    if isinstance(data, dict):
        return data

    if isinstance(data, list):
        result = {}

        for airline in data:
            if isinstance(airline, dict):
                name = airline.get("name") or airline.get("airline")

                if name:
                    result[name] = airline

        return result

    return {}


airlines = get_airlines(airlines_data)


# ============================================================
# DEFAULT AIRLINES
# ============================================================

if not airlines:
    airlines = {
        "Emirates": {
            "description": "Cabin Crew recruitment requirements for Emirates.",
            "requirements": {
                "age": 21,
                "height": 160,
                "reach": 212,
                "english": True,
                "education": True,
                "experience": 1,
                "swimming": True,
                "tattoos": False,
            },
        },

        "Qatar Airways": {
            "description": "Cabin Crew recruitment requirements for Qatar Airways.",
            "requirements": {
                "age": 21,
                "height": 160,
                "reach": 212,
                "english": True,
                "education": True,
                "experience": 1,
                "swimming": True,
                "tattoos": False,
            },
        },

        "Etihad Airways": {
            "description": "Cabin Crew recruitment requirements for Etihad Airways.",
            "requirements": {
                "age": 21,
                "height": 163,
                "reach": 210,
                "english": True,
                "education": True,
                "experience": 1,
                "swimming": True,
                "tattoos": False,
            },
        },
    }


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background: #0e1117;
    }

    /* Header */
    .hero {
        background: linear-gradient(
            135deg,
            #0758c9 0%,
            #087cf0 50%,
            #00a6ff 100%
        );

        padding: 35px;
        border-radius: 22px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }

    .hero h1 {
        margin: 0;
        font-size: 42px;
        font-weight: 800;
    }

    .hero p {
        margin-top: 10px;
        font-size: 18px;
        opacity: 0.95;
    }

    /* Section cards */
    .card {
        background: #171b24;
        border: 1px solid #292f3b;
        border-radius: 18px;
        padding: 25px;
        margin: 12px 0;
    }

    .card h2,
    .card h3 {
        margin-top: 0;
    }

    /* Requirement result */
    .requirement {
        background: #202631;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
    }

    .pass {
        border-left: 5px solid #2ecc71;
    }

    .fail {
        border-left: 5px solid #ff5252;
    }

    .warning {
        border-left: 5px solid #f5b942;
    }

    .result-title {
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .score {
        font-size: 42px;
        font-weight: 800;
        margin: 10px 0;
    }

    .small {
        color: #aab2bf;
        font-size: 14px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #11151c;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe(value):
    """Safely escape text before putting it inside HTML."""
    return html.escape(str(value))


def find_value(data, *keys, default=None):
    """Find the first available key in a dictionary."""
    if not isinstance(data, dict):
        return default

    for key in keys:
        if key in data:
            return data[key]

    return default


def get_requirements(airline):
    """Extract requirement dictionary from airline data."""

    data = airlines.get(airline, {})

    requirements = data.get("requirements", {})

    if isinstance(requirements, dict):
        return requirements

    return {}


def get_airline_description(airline):
    data = airlines.get(airline, {})

    return find_value(
        data,
        "description",
        "desc",
        "summary",
        default=f"Cabin Crew recruitment requirements for {airline}.",
    )


# ============================================================
# REQUIREMENT NORMALIZATION
# ============================================================

def requirement_age(req):
    return find_value(
        req,
        "age",
        "minimum_age",
        "min_age",
        default=None,
    )


def requirement_height(req):
    return find_value(
        req,
        "height",
        "minimum_height",
        "min_height",
        default=None,
    )


def requirement_reach(req):
    return find_value(
        req,
        "reach",
        "arm_reach",
        "minimum_reach",
        "min_reach",
        default=None,
    )


def requirement_experience(req):
    return find_value(
        req,
        "experience",
        "minimum_experience",
        "min_experience",
        default=None,
    )


def requirement_english(req):
    return find_value(
        req,
        "english",
        "english_required",
        default=None,
    )


def requirement_education(req):
    return find_value(
        req,
        "education",
        "education_required",
        default=None,
    )


def requirement_swimming(req):
    return find_value(
        req,
        "swimming",
        "swimming_required",
        default=None,
    )


def requirement_tattoos(req):
    return find_value(
        req,
        "tattoos",
        "visible_tattoos",
        "no_tattoos",
        default=None,
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:10px 0 20px 0;
    ">
        <div style="font-size:42px;">✈️</div>
        <h2 style="margin:0;">CabinCrewHub</h2>
        <p style="color:#9da6b5;">
            Your cabin crew preparation companion
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigate",
    [
        "🔎 Airline Checker",
        "🎤 Interview Trainer",
    ],
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "CabinCrewHub helps applicants prepare for airline recruitment."
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>✈️ CabinCrewHub</h1>
        <p>
            Your cabin crew preparation and airline application companion.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AIRLINE CHECKER
# ============================================================

if page == "🔎 Airline Checker":

    st.markdown(
        """
        <div class="card">
            <h2>🔎 Airline Application Checker</h2>
            <p>
                Enter your information to compare your profile with
                the requirements currently stored for the selected airline.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    airline_names = list(airlines.keys())

    if not airline_names:
        st.error("No airlines were found in airlines.json.")
        st.stop()

    airline = st.selectbox(
        "Select an airline",
        airline_names,
    )

    req = get_requirements(airline)

    st.markdown(
        f"""
        <div class="card">
            <h2>✈️ {safe(airline)}</h2>
            <p>{safe(get_airline_description(airline))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # PERSONAL INFORMATION
    # --------------------------------------------------------

    st.subheader("👤 Your Profile")

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
                "Fluent",
                "Very Fluent",
                "Intermediate",
                "Basic",
                "Not fluent",
            ],
        )

        education = st.selectbox(
            "Education requirement",
            [
                "Meets requirement",
                "Does not meet requirement",
            ],
        )

        swimming = st.selectbox(
            "Can you swim?",
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

    # --------------------------------------------------------
    # CHECK BUTTON
    # --------------------------------------------------------

    st.markdown("")

    check = st.button(
        "🔍 Check My Profile",
        type="primary",
        use_container_width=True,
    )

    if check:

        results = []

        # ----------------------------------------------------
        # AGE
        # ----------------------------------------------------

        minimum_age = requirement_age(req)

        if minimum_age is not None:

            try:
                minimum_age = float(minimum_age)

                passed = age >= minimum_age

                results.append(
                    {
                        "name": "Age",
                        "passed": passed,
                        "detail": (
                            f"Your age: {age} | "
                            f"Minimum: {minimum_age:g}"
                        ),
                    }
                )

            except (ValueError, TypeError):
                pass

        # ----------------------------------------------------
        # HEIGHT
        # ----------------------------------------------------

        minimum_height = requirement_height(req)

        if minimum_height is not None:

            try:
                minimum_height = float(minimum_height)

                passed = height >= minimum_height

                results.append(
                    {
                        "name": "Height",
                        "passed": passed,
                        "detail": (
                            f"Your height: {height} cm | "
                            f"Minimum: {minimum_height:g} cm"
                        ),
                    }
                )

            except (ValueError, TypeError):
                pass

        # ----------------------------------------------------
        # REACH
        # ----------------------------------------------------

        minimum_reach = requirement_reach(req)

        if minimum_reach is not None:

            try:
                minimum_reach = float(minimum_reach)

                passed = reach >= minimum_reach

                results.append(
                    {
                        "name": "Arm reach",
                        "passed": passed,
                        "detail": (
                            f"Your reach: {reach} cm | "
                            f"Minimum: {minimum_reach:g} cm"
                        ),
                    }
                )

            except (ValueError, TypeError):
                pass

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        minimum_experience = requirement_experience(req)

        if minimum_experience is not None:

            try:
                minimum_experience = float(minimum_experience)

                passed = experience >= minimum_experience

                results.append(
                    {
                        "name": "Experience",
                        "passed": passed,
                        "detail": (
                            f"Your experience: {experience:g} years | "
                            f"Minimum: {minimum_experience:g} years"
                        ),
                    }
                )

            except (ValueError, TypeError):
                pass

        # ----------------------------------------------------
        # ENGLISH
        # ----------------------------------------------------

        english_required = requirement_english(req)

        if english_required is True:

            passed = english in [
                "Fluent",
                "Very Fluent",
            ]

            results.append(
                {
                    "name": "English",
                    "passed": passed,
                    "detail": (
                        f"Your level: {english} | "
                        "Fluent English expected"
                    ),
                }
            )

        # ----------------------------------------------------
        # EDUCATION
        # ----------------------------------------------------

        education_required = requirement_education(req)

        if education_required is not None:

            if education_required is True:

                passed = education == "Meets requirement"

                results.append(
                    {
                        "name": "Education",
                        "passed": passed,
                        "detail": education,
                    }
                )

        # ----------------------------------------------------
        # SWIMMING
        # ----------------------------------------------------

        swimming_required = requirement_swimming(req)

        if swimming_required is True:

            passed = swimming == "Yes"

            results.append(
                {
                    "name": "Swimming",
                    "passed": passed,
                    "detail": (
                        "Able to swim"
                        if passed
                        else "Swimming requirement not met"
                    ),
                }
            )

        # ----------------------------------------------------
        # TATTOOS
        # ----------------------------------------------------

        tattoo_requirement = requirement_tattoos(req)

        if tattoo_requirement is not None:

            # Different JSON formats can mean different things.
            if tattoo_requirement is False:

                passed = tattoos == "No"

                results.append(
                    {
                        "name": "Visible tattoos",
                        "passed": passed,
                        "detail": (
                            "No visible tattoos"
                            if passed
                            else "Visible tattoos reported"
                        ),
                    }
                )

            elif tattoo_requirement is True:

                # In this format True means tattoos are allowed.
                results.append(
                    {
                        "name": "Visible tattoos",
                        "passed": True,
                        "detail": "Your airline data allows tattoos.",
                    }
                )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        st.markdown("---")

        if results:

            passed_count = sum(
                1 for result in results
                if result["passed"]
            )

            total_count = len(results)

            percentage = round(
                (passed_count / total_count) * 100
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="result-title">
                        📊 Application Check
                    </div>

                    <div class="score">
                        {percentage}%
                    </div>

                    <p>
                        You currently meet
                        <strong>{passed_count}</strong>
                        of
                        <strong>{total_count}</strong>
                        stored requirements for
                        <strong>{safe(airline)}</strong>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # REQUIREMENT BREAKDOWN
            # ------------------------------------------------

            st.subheader("Requirement Breakdown")

            for result in results:

                if result["passed"]:

                    st.markdown(
                        f"""
                        <div class="requirement pass">
                            <strong>✅ {safe(result["name"])}</strong>
                            <br>
                            <span class="small">
                                {safe(result["detail"])}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="requirement fail">
                            <strong>❌ {safe(result["name"])}</strong>
                            <br>
                            <span class="small">
                                {safe(result["detail"])}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        else:

            st.warning(
                "No structured requirements were found for this airline."
            )


# ============================================================
# INTERVIEW TRAINER
# ============================================================

elif page == "🎤 Interview Trainer":

    st.markdown(
        """
        <div class="card">
            <h2>🎤 Cabin Crew Interview Trainer</h2>
            <p>
                Practice common cabin crew interview questions and
                improve your answers before your assessment.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # NORMALIZE QUESTIONS
    # --------------------------------------------------------

    questions = []

    if isinstance(questions_data, list):
        questions = questions_data

    elif isinstance(questions_data, dict):

        possible_questions = (
            questions_data.get("questions")
            or questions_data.get("interview_questions")
            or []
        )

        if isinstance(possible_questions, list):
            questions = possible_questions

    # --------------------------------------------------------
    # FALLBACK QUESTIONS
    # --------------------------------------------------------

    if not questions:

        questions = [
            {
                "question": "Tell me about yourself.",
                "category": "Introduction",
            },
            {
                "question": "Why do you want to become cabin crew?",
                "category": "Motivation",
            },
            {
                "question": "Why do you want to work for this airline?",
                "category": "Motivation",
            },
            {
                "question": "Tell me about a time you dealt with a difficult customer.",
                "category": "Customer Service",
            },
            {
                "question": "How would you handle an angry passenger?",
                "category": "Customer Service",
            },
            {
                "question": "How would you handle a conflict with another crew member?",
                "category": "Teamwork",
            },
            {
                "question": "What does excellent customer service mean to you?",
                "category": "Customer Service",
            },
            {
                "question": "How would you respond to an emergency on board?",
                "category": "Safety",
            },
            {
                "question": "What are the most important responsibilities of cabin crew?",
                "category": "Cabin Crew",
            },
            {
                "question": "Why should we hire you?",
                "category": "General",
            },
        ]

    # --------------------------------------------------------
    # QUESTION EXTRACTION
    # --------------------------------------------------------

    def get_question_text(item):

        if isinstance(item, str):
            return item

        if isinstance(item, dict):

            return (
                item.get("question")
                or item.get("text")
                or item.get("prompt")
                or "Interview question"
            )

        return "Interview question"

    def get_category(item):

        if isinstance(item, dict):

            return (
                item.get("category")
                or item.get("type")
                or "General"
            )

        return "General"

    categories = sorted(
        set(get_category(q) for q in questions)
    )

    selected_category = st.selectbox(
        "Choose a category",
        ["All"] + categories,
    )

    filtered_questions = questions

    if selected_category != "All":

        filtered_questions = [
            q
            for q in questions
            if get_category(q) == selected_category
        ]

    if not filtered_questions:

        st.info("No questions available for this category.")

    else:

        question_number = st.number_input(
            "Question",
            min_value=1,
            max_value=len(filtered_questions),
            value=1,
            step=1,
        )

        current_question = filtered_questions[
            question_number - 1
        ]

        question_text = get_question_text(current_question)

        st.markdown(
            f"""
            <div class="card">
                <p class="small">
                    {safe(get_category(current_question))}
                </p>

                <h2>
                    {safe(question_text)}
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        answer = st.text_area(
            "Your answer",
            height=220,
            placeholder=(
                "Type your answer here. "
                "For experience-based questions, "
                "try using the STAR method: "
                "Situation → Task → Action → Result."
            ),
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💡 Show Answer Tips",
                use_container_width=True,
            ):

                st.info(
                    """
                    **Interview tip**

                    Structure your answer clearly.

                    **Situation** — What was happening?

                    **Task** — What were you responsible for?

                    **Action** — What did you personally do?

                    **Result** — What happened afterwards?

                    Keep your answer positive, specific and
                    focused on customer service, teamwork,
                    communication and safety.
                    """
                )

        with col2:

            if st.button(
                "📝 Check My Answer",
                use_container_width=True,
            ):

                if not answer.strip():

                    st.warning(
                        "Please write an answer first."
                    )

                else:

                    answer_length = len(
                        answer.strip().split()
                    )

                    feedback = []

                    if answer_length < 30:

                        feedback.append(
                            "Your answer is quite short. "
                            "Add a specific example."
                        )

                    elif answer_length <= 120:

                        feedback.append(
                            "Your answer has a useful length. "
                            "Make sure every sentence adds value."
                        )

                    else:

                        feedback.append(
                            "Your answer is detailed. "
                            "Make sure it stays focused."
                        )

                    lower_answer = answer.lower()

                    keywords = [
                        "customer",
                        "team",
                        "safety",
                        "communication",
                        "passenger",
                        "service",
                    ]

                    found = [
                        word
                        for word in keywords
                        if word in lower_answer
                    ]

                    if found:

                        feedback.append(
                            "Good: your answer includes "
                            "relevant cabin-crew themes such as "
                            + ", ".join(found)
                            + "."
                        )

                    else:

                        feedback.append(
                            "Consider connecting your answer "
                            "to customer service, teamwork, "
                            "communication or safety where relevant."
                        )

                    for item in feedback:
                        st.write("• " + item)

        # ----------------------------------------------------
        # STAR REMINDER
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="card">
                <h3>⭐ STAR Method</h3>

                <p>
                    <strong>S — Situation:</strong>
                    What was happening?
                </p>

                <p>
                    <strong>T — Task:</strong>
                    What were you responsible for?
                </p>

                <p>
                    <strong>A — Action:</strong>
                    What did you personally do?
                </p>

                <p>
                    <strong>R — Result:</strong>
                    What was the outcome?
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        padding:35px 0 10px 0;
        color:#737c8c;
        font-size:13px;
    ">
        ✈️ CabinCrewHub
        <br>
        Cabin crew preparation made simpler.
    </div>
    """,
    unsafe_allow_html=True,
)
