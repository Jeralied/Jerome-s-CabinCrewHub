import streamlit as st
import json
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="CabinCrewHub",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .hero {
        padding: 35px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0b1f3a, #173f67);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
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
        background: #f8fafc;
        border: 1px solid #e2e8f0;
    }

    .check {
        font-size: 20px;
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


# -----------------------------
# LOAD AIRLINE DATA
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
AIRLINE_FILE = BASE_DIR / "airlines.json"


def load_airlines():
    try:
        with open(AIRLINE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("airlines.json was not found.")
        return {}
    except json.JSONDecodeError:
        st.error("airlines.json contains invalid JSON.")
        return {}


airlines = load_airlines()


# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>✈️ CabinCrewHub</h1>
    <p>
        Check cabin crew requirements and prepare for your airline application.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# NAVIGATION
# -----------------------------
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
        "Enter your information below and compare your profile "
        "with the published cabin crew requirements."
    )

    if not airlines:
        st.warning("No airline information is available yet.")
        st.stop()

    airline_names = list(airlines.keys())

    selected_airline = st.selectbox(
        "Select an airline",
        airline_names
    )

    airline = airlines[selected_airline]

    st.markdown(
        f"""
        <div class="card">
            <h2>✈️ {selected_airline}</h2>
            <p>{airline.get("description", "")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
            ["Fluent", "Good", "Basic", "None"]
        )

        education = st.selectbox(
            "Education",
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
        ["Yes", "No", "Not sure"]
    )

    tattoos = st.selectbox(
        "Visible tattoos while wearing the airline uniform?",
        ["No", "Yes", "Not sure"]
    )

    st.divider()

    if st.button(
        "🔍 Check My Requirements",
        type="primary",
        use_container_width=True
    ):

        results = []

        # AGE
        if "min_age" in airline:
            if age >= airline["min_age"]:
                results.append(
                    ("✓", "Age", "Meets requirement", "success")
                )
            else:
                results.append(
                    ("✗", "Age", f"Minimum age is {airline['min_age']}", "error")
                )

        # HEIGHT
        if "min_height" in airline:
            if height >= airline["min_height"]:
                results.append(
                    ("✓", "Height", "Meets requirement", "success")
                )
            else:
                results.append(
                    ("✗", "Height",
                     f"Minimum height is {airline['min_height']} cm",
                     "error")
                )

        # REACH
        if "min_reach" in airline:
            if reach >= airline["min_reach"]:
                results.append(
                    ("✓", "Arm Reach", "Meets requirement", "success")
                )
            else:
                results.append(
                    ("✗", "Arm Reach",
                     f"Minimum reach is {airline['min_reach']} cm",
                     "error")
                )

        # ENGLISH
        if airline.get("english_required", False):

            if english == "Fluent":
                results.append(
                    ("✓", "English", "Fluent English selected", "success")
                )
            else:
                results.append(
                    ("⚠", "English",
                     "Fluent English is required — verify your level",
                     "warning")
                )

        # EDUCATION
        if airline.get("secondary_education_required", False):

            valid_education = [
                "Secondary school / Grade 12",
                "Diploma",
                "Bachelor's degree",
                "Master's degree"
            ]

            if education in valid_education:
                results.append(
                    ("✓", "Education",
                     "Secondary education or higher selected",
                     "success")
                )
            else:
                results.append(
                    ("✗", "Education",
                     "Secondary education is required",
                     "error")
                )

        # EXPERIENCE
        if airline.get("experience_required", False):

            required_experience = airline.get(
                "minimum_experience_years", 1
            )

            if experience >= required_experience:
                results.append(
                    ("✓", "Experience",
                     f"{experience:g} years entered",
                     "success")
                )
            else:
                results.append(
                    ("✗", "Experience",
                     f"At least {required_experience} year(s) required",
                     "error")
                )

        # SWIMMING
        if airline.get("swimming_required", False):

            if swimming == "Yes":
                results.append(
                    ("✓", "Swimming",
                     "Swimming ability confirmed",
                     "success")
                )
            elif swimming == "No":
                results.append(
                    ("✗", "Swimming",
                     "Swimming requirement not met",
                     "error")
                )
            else:
                results.append(
                    ("⚠", "Swimming",
                     "Verify swimming requirement",
                     "warning")
                )

        # TATTOOS
        if airline.get("no_visible_tattoos", False):

            if tattoos == "No":
                results.append(
                    ("✓", "Visible Tattoos",
                     "No visible tattoos selected",
                     "success")
                )
            elif tattoos == "Yes":
                results.append(
                    ("✗", "Visible Tattoos",
                     "Visible tattoos may conflict with this requirement",
                     "error")
                )
            else:
                results.append(
                    ("⚠", "Visible Tattoos",
                     "Verify the airline's uniform policy",
                     "warning")
                )

        # -----------------------------
        # RESULTS
        # -----------------------------

        st.subheader("📋 Requirement Check")

        for icon, requirement, message, status in results:

            st.markdown(
                f"""
                <div class="result-box">
                    <span class="check">{icon} {requirement}</span>
                    <br>
                    <span class="small-text">{message}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        passed = sum(1 for r in results if r[3] == "success")
        failed = sum(1 for r in results if r[3] == "error")
        warnings = sum(1 for r in results if r[3] == "warning")

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("✓ Meets", passed)

        with c2:
            st.metric("⚠ Verify", warnings)

        with c3:
            st.metric("✗ Does not meet", failed)

        st.info(
            "This tool is a requirement checklist, not a guarantee of "
            "employment or selection. Always verify the current official "
            "airline vacancy before applying."
        )


# ============================================================
# INTERVIEW TRAINER
# ============================================================

elif page == "🎤 Interview Trainer":

    st.subheader("🎤 Cabin Crew Interview Trainer")

    st.write(
        "This section will contain cabin crew interview questions, "
        "answer evaluation and feedback."
    )

    st.info(
        "🚧 Interview Trainer is coming next. "
        "We are building the Airline Checker first."
    )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "✈️ CabinCrewHub • Built to help aspiring cabin crew applicants prepare."
)
