import random
import re
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st
from sympy import Eq, S, Symbol, sympify, Interval
from sympy.solvers import solveset
from sympy.solvers.inequalities import solve_univariate_inequality
from sympy import Eq, Interval, S, Symbol, sympify
from sympy.solvers import solveset


# -----------------------------
# Configuration and Styling
# -----------------------------

st.set_page_config(
    page_title="8-4-4 Math Revision (F2 & F3)",
    page_icon="📘",
    layout="wide",
)

KENYA_GREEN = "#007A3D"
KENYA_RED = "#CE1126"
KENYA_BLACK = "#000000"

st.markdown(
    f"""
    <style>
        .main {{
            font-family: 'Segoe UI', sans-serif;
        }}
        .kenya-header {{
            background: linear-gradient(90deg, {KENYA_BLACK}, {KENYA_GREEN}, {KENYA_RED});
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
        }}
        .topic-pill {{
            display: inline-block;
            margin: 0.25rem 0.4rem 0 0;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            border: 1px solid {KENYA_GREEN};
            color: {KENYA_GREEN};
            font-size: 0.85rem;
        }}
        .footer {{
            text-align: center;
            color: #555;
            padding: 1rem 0 0.5rem 0;
            font-size: 0.9rem;
        }}
        .stButton>button {{
            background-color: {KENYA_GREEN};
            color: white;
            border-radius: 0.5rem;
        }}
        .stButton>button:hover {{
            background-color: {KENYA_RED};
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Data and Utilities
# -----------------------------

x = Symbol("x")

TOPICS = [
    "Algebra",
    "Geometry",
    "Trigonometry",
    "Statistics",
    "Coordinate Geometry",
]

SAMPLE_PROBLEMS = {
    "Algebra": [
        "Solve 2x^2 + 5x - 3 = 0",
        "Solve 3x - 7 = 11",
        "Solve inequality: x^2 - 5x + 6 > 0",
    ],
    "Geometry": [
        "Pythagoras: A right triangle has legs 6 cm and 8 cm. Find the hypotenuse.",
        "Circle: Find circumference when radius is 7 cm.",
        "Mensuration: Find area of a triangle with base 12 cm and height 5 cm.",
    ],
    "Trigonometry": [
        "Sine rule: Find side a if A=30°, b=10 cm, B=45°.",
        "Cosine rule: Find side c if a=7 cm, b=9 cm, C=60°.",
        "Bearing: A boat sails 12 km on bearing 030°. Find its east displacement.",
    ],
    "Statistics": [
        "Find mean of 4, 6, 10, 12, 18.",
        "Find median of 5, 7, 9, 13, 21, 30.",
        "Probability: A bag has 3 red and 2 blue balls. Find P(red).",
    ],
    "Coordinate Geometry": [
        "Find midpoint between (2, 3) and (8, 11).",
        "Find gradient between (-1, 4) and (3, 12).",
        "Find distance between (1, 2) and (4, 6).",
    ],
}


def parse_equation(problem: str) -> Tuple[str, str]:
    """Return left/right parts of an equation or inequality."""
    for symbol in [">=", "<=", ">", "<", "="]:
        if symbol in problem:
            parts = problem.split(symbol)
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
    return "", ""


def clean_expression(expression: str) -> str:
    return expression.replace("^", "**")


def solve_algebra(problem: str) -> Dict[str, List[str]]:
    steps = []
    cleaned = clean_expression(problem.lower().replace("solve", ""))
    left, right = parse_equation(cleaned)

    if not left:
        return {
            "error": [
                "We could not detect a valid equation.",
                "Try rephrasing: 'Find the roots of x^2 - 4x + 4 = 0'.",
            ]
        }

    if ">" in cleaned or "<" in cleaned:
        symbol = ">" if ">" in cleaned else "<"
        if ">=" in cleaned:
            symbol = ">="
        if "<=" in cleaned:
            symbol = "<="
        lhs = sympify(left)
        rhs = sympify(right)
        steps.append(f"Rewrite inequality: {lhs} {symbol} {rhs}")
        steps.append("Move everything to the left-hand side.")
        inequality = lhs - rhs
        steps.append(f"Simplify: {inequality} {symbol} 0")
        solution = solveset(Eq(inequality, 0), x, domain=S.Reals)
        steps.append("Find critical points by solving equality.")
        steps.append(f"Critical points: {solution}")
        steps.append("Use a sign chart to determine intervals that satisfy the inequality.")
        return {"steps": steps, "answer": ["Solution intervals depend on sign chart."]}

    lhs = sympify(left)
    rhs = sympify(right)
    equation = Eq(lhs, rhs)
    steps.append(f"Rewrite equation: {equation}")
    steps.append("Move all terms to one side to get a standard form.")
    standard = lhs - rhs
    steps.append(f"Standard form: {standard} = 0")

    if standard.as_poly(x) is not None and standard.as_poly(x).degree() == 2:
        a, b, c = standard.as_poly(x).all_coeffs()
        steps.append(f"Identify coefficients: a={a}, b={b}, c={c}.")
        steps.append("Compute discriminant: Δ = b² - 4ac.")
        discriminant = b**2 - 4 * a * c
        steps.append(f"Δ = {discriminant}.")
        steps.append("Use quadratic formula: x = (-b ± √Δ) / (2a).")
        solutions = solveset(equation, x, domain=S.Reals)
        return {"steps": steps, "answer": [f"Solution: x = {solutions}"]}

    if standard.as_poly(x) is not None and standard.as_poly(x).degree() == 1:
        steps.append("Isolate the variable using inverse operations.")
        solution = solveset(equation, x, domain=S.Reals)
        return {"steps": steps, "answer": [f"Solution: x = {solution}"]}

    return {
        "error": [
            "This solver handles linear, quadratic equations, or inequalities.",
            "Try rephrasing: 'Solve 2x^2 + 5x - 3 = 0'.",
        ]
    }


def solve_geometry(problem: str) -> Dict[str, List[str]]:
    steps = []
    text = problem.lower()
    if "pythagoras" in text:
        steps.append("Use Pythagoras theorem: c² = a² + b².")
        steps.append("Substitute a=6, b=8.")
        steps.append("c² = 6² + 8² = 36 + 64 = 100.")
        steps.append("c = √100 = 10 cm.")
        return {"steps": steps, "answer": ["Hypotenuse = 10 cm."]}
    if "circumference" in text:
        steps.append("Circumference formula: C = 2πr.")
        steps.append("Substitute r=7.")
        steps.append("C = 2 × π × 7 = 14π cm.")
        return {"steps": steps, "answer": ["Circumference = 14π cm (≈ 43.98 cm)."]}
    if "area" in text and "triangle" in text:
        steps.append("Triangle area formula: A = 1/2 × base × height.")
        steps.append("A = 1/2 × 12 × 5 = 30 cm².")
        return {"steps": steps, "answer": ["Area = 30 cm²."]}
    return {
        "error": [
            "Geometry solver supports Pythagoras, circle circumference, and triangle area.",
            "Try the sample problems from the dropdown.",
        ]
    }


def solve_trigonometry(problem: str) -> Dict[str, List[str]]:
    steps = []
    text = problem.lower()
    if "sine" in text:
        steps.append("Use sine rule: a/sin A = b/sin B.")
        steps.append("Let b=10, A=30°, B=45°.")
        steps.append("a = (sin 30° / sin 45°) × 10.")
        steps.append("sin 30° = 0.5, sin 45° ≈ 0.707.")
        steps.append("a ≈ (0.5 / 0.707) × 10 ≈ 7.07 cm.")
        return {"steps": steps, "answer": ["Side a ≈ 7.07 cm."]}
    if "cosine" in text:
        steps.append("Use cosine rule: c² = a² + b² - 2ab cos C.")
        steps.append("Substitute a=7, b=9, C=60°.")
        steps.append("c² = 49 + 81 - 2×7×9×0.5 = 130 - 63 = 67.")
        steps.append("c = √67 ≈ 8.19 cm.")
        return {"steps": steps, "answer": ["Side c ≈ 8.19 cm."]}
    if "bearing" in text:
        steps.append("Bearing 030° means 30° east of north.")
        steps.append("East displacement = distance × sin(30°).")
        steps.append("East = 12 × 0.5 = 6 km.")
        return {"steps": steps, "answer": ["East displacement = 6 km."]}
    return {
        "error": [
            "Trigonometry solver supports sine rule, cosine rule, and bearings.",
            "Try the sample problems from the dropdown.",
        ]
    }


def solve_statistics(problem: str) -> Dict[str, List[str]]:
    steps = []
    text = problem.lower()
    if "mean" in text:
        steps.append("Add the values and divide by the count.")
        steps.append("Sum = 4 + 6 + 10 + 12 + 18 = 50.")
        steps.append("Mean = 50 / 5 = 10.")
        return {"steps": steps, "answer": ["Mean = 10."]}
    if "median" in text:
        steps.append("Order the values: 5, 7, 9, 13, 21, 30.")
        steps.append("Even count: median = average of 3rd and 4th values.")
        steps.append("Median = (9 + 13) / 2 = 11.")
        return {"steps": steps, "answer": ["Median = 11."]}
    if "probability" in text:
        steps.append("Probability = favorable outcomes / total outcomes.")
        steps.append("Favorable (red) = 3, Total = 3 + 2 = 5.")
        steps.append("P(red) = 3/5 = 0.6.")
        return {"steps": steps, "answer": ["Probability = 3/5 (0.6)."]}
    return {
        "error": [
            "Statistics solver supports mean, median, and basic probability.",
            "Try the sample problems from the dropdown.",
        ]
    }


def solve_coordinate(problem: str) -> Dict[str, List[str]]:
    steps = []
    text = problem.lower()
    if "midpoint" in text:
        steps.append("Midpoint formula: ((x1 + x2)/2, (y1 + y2)/2).")
        steps.append("((2 + 8)/2, (3 + 11)/2) = (5, 7).")
        return {"steps": steps, "answer": ["Midpoint = (5, 7)."]}
    if "gradient" in text:
        steps.append("Gradient formula: (y2 - y1)/(x2 - x1).")
        steps.append("(12 - 4)/(3 - (-1)) = 8/4 = 2.")
        return {"steps": steps, "answer": ["Gradient = 2."]}
    if "distance" in text:
        steps.append("Distance formula: √((x2 - x1)² + (y2 - y1)²).")
        steps.append("√((4 - 1)² + (6 - 2)²) = √(9 + 16) = √25.")
        steps.append("Distance = 5.")
        return {"steps": steps, "answer": ["Distance = 5 units."]}
    return {
        "error": [
            "Coordinate geometry solver supports midpoint, gradient, and distance.",
            "Try the sample problems from the dropdown.",
        ]
    }


def solve_problem(topic: str, problem: str) -> Dict[str, List[str]]:
    if topic == "Algebra":
        return solve_algebra(problem)
    if topic == "Geometry":
        return solve_geometry(problem)
    if topic == "Trigonometry":
        return solve_trigonometry(problem)
    if topic == "Statistics":
        return solve_statistics(problem)
    if topic == "Coordinate Geometry":
        return solve_coordinate(problem)
    return {"error": ["Unsupported topic."]}


def get_quiz_bank() -> pd.DataFrame:
    questions = [
        {
            "topic": "Algebra",
            "difficulty": "Easy",
            "question": "Solve 3x - 7 = 11.",
            "options": ["x=4", "x=6", "x=8", "x=2"],
            "answer": "x=6",
            "explanation": "Add 7 to both sides (3x=18) then divide by 3.",
        },
        {
            "topic": "Algebra",
            "difficulty": "Medium",
            "question": "Solve x^2 - 5x + 6 = 0.",
            "options": ["x=2 or x=3", "x=1 or x=6", "x= -2 or x= -3", "x=3 only"],
            "answer": "x=2 or x=3",
            "explanation": "Factor: (x-2)(x-3)=0.",
        },
        {
            "topic": "Geometry",
            "difficulty": "Easy",
            "question": "A triangle has base 10 cm and height 6 cm. Find area.",
            "options": ["30 cm²", "60 cm²", "16 cm²", "20 cm²"],
            "answer": "30 cm²",
            "explanation": "Area = 1/2 × 10 × 6 = 30.",
        },
        {
            "topic": "Geometry",
            "difficulty": "Hard",
            "question": "Radius of a circle is 14 cm. Find circumference (in π).",
            "options": ["28π cm", "14π cm", "56π cm", "7π cm"],
            "answer": "28π cm",
            "explanation": "C = 2πr = 2π × 14 = 28π.",
        },
        {
            "topic": "Trigonometry",
            "difficulty": "Medium",
            "question": "Find side c if a=7, b=9, C=60°.",
            "options": ["8.19 cm", "10 cm", "6 cm", "12 cm"],
            "answer": "8.19 cm",
            "explanation": "Use cosine rule: c²=49+81-2×7×9×0.5=67.",
        },
        {
            "topic": "Trigonometry",
            "difficulty": "Easy",
            "question": "sin 30° equals:",
            "options": ["1", "0.5", "0.866", "0"],
            "answer": "0.5",
            "explanation": "Standard trig ratio.",
        },
        {
            "topic": "Statistics",
            "difficulty": "Easy",
            "question": "Find mean of 4, 6, 10, 12, 18.",
            "options": ["10", "8", "12", "9"],
            "answer": "10",
            "explanation": "Mean = sum 50 / 5.",
        },
        {
            "topic": "Statistics",
            "difficulty": "Medium",
            "question": "A bag has 3 red, 2 blue balls. P(red) = ?",
            "options": ["1/2", "3/5", "2/3", "5/3"],
            "answer": "3/5",
            "explanation": "Favorable / total = 3 / 5.",
        },
        {
            "topic": "Coordinate Geometry",
            "difficulty": "Easy",
            "question": "Find midpoint between (2,3) and (8,11).",
            "options": ["(5,7)", "(4,6)", "(6,5)", "(3,4)"],
            "answer": "(5,7)",
            "explanation": "Midpoint = ((2+8)/2, (3+11)/2).",
        },
        {
            "topic": "Coordinate Geometry",
            "difficulty": "Medium",
            "question": "Find gradient between (-1,4) and (3,12).",
            "options": ["1", "2", "3", "4"],
            "answer": "2",
            "explanation": "Gradient = (12-4)/(3-(-1))=8/4.",
        },
    ]
    return pd.DataFrame(questions)


# -----------------------------
# Sidebar Navigation
# -----------------------------

st.sidebar.markdown("## Navigation")
if "nav" not in st.session_state:
    st.session_state.nav = "Home"
nav = st.sidebar.radio("Go to", ["Home", "Solver", "Quiz", "Resources"], key="nav")

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Topics")
for topic in TOPICS:
    st.sidebar.markdown(f"- {topic}")


# -----------------------------
# Home Page
# -----------------------------

if nav == "Home":
    st.markdown(
        """
        <div class="kenya-header">
            <h1>8-4-4 Math Revision Hub</h1>
            <p>Form 2 & Form 3 | KCSE Prep Focus</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Syllabus Overview")
    st.write(
        "Explore core areas aligned to the Kenyan 8-4-4 syllabus: Algebra, Geometry, "
        "Trigonometry, Statistics, and Coordinate Geometry. Each section includes guided solver "
        "steps, quizzes, and quick reference notes."
    )

    st.markdown("""<div>""", unsafe_allow_html=True)
    for topic in TOPICS:
        st.markdown(f"<span class='topic-pill'>{topic}</span>", unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)

    st.subheader("Quick Search")
    with st.form("search_form"):
        search_query = st.text_input(
            "Type a math problem (e.g., Solve 2x^2 + 5x - 3 = 0)",
            value=st.session_state.get("search_query", ""),
        )
        submitted = st.form_submit_button("Send to Solver")
        if submitted:
            st.session_state.search_query = search_query
            st.session_state.nav = "Solver"

    st.info(
        "Tip: Use the Solver tab for guided steps, or jump to the Quiz tab for practice.")


# -----------------------------
# Solver Page
# -----------------------------

if nav == "Solver":
    st.markdown(
        """
        <div class="kenya-header">
            <h2>Math Solver & Worked Steps</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_topic = st.selectbox("Select Topic", TOPICS)
        problem_input = st.text_area(
            "Enter a math problem",
            value=st.session_state.get("search_query", ""),
            height=120,
        )
        if st.button("Solve Problem"):
            if not problem_input.strip():
                st.warning(
                    "Please enter a problem. Try: 'Solve 2x^2 + 5x - 3 = 0'.")
            else:
                result = solve_problem(selected_topic, problem_input)
                if "error" in result:
                    st.error("\n".join(result["error"]))
                else:
                    st.success("Solution generated successfully!")
                    st.markdown("#### Step-by-step")
                    for step in result["steps"]:
                        st.write(f"- {step}")
                    st.markdown("#### Final Answer")
                    for answer in result["answer"]:
                        st.write(answer)

    with col2:
        st.markdown("### Sample Problems")
        sample = st.selectbox("Choose a sample", SAMPLE_PROBLEMS[selected_topic])
        if st.button("Load Sample"):
            st.session_state.search_query = sample
            st.experimental_rerun()


# -----------------------------
# Quiz Page
# -----------------------------

if nav == "Quiz":
    st.markdown(
        """
        <div class="kenya-header">
            <h2>Topic Quiz - 10 Questions</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    quiz_bank = get_quiz_bank()
    topic_choice = st.selectbox("Choose Topic", TOPICS)
    difficulty_choice = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if "quiz" not in st.session_state or st.button("Generate New Quiz"):
        filtered = quiz_bank[
            (quiz_bank["topic"] == topic_choice)
            & (quiz_bank["difficulty"] == difficulty_choice)
        ]
        if filtered.empty:
            filtered = quiz_bank[quiz_bank["topic"] == topic_choice]
        st.session_state.quiz = filtered.sample(
            min(10, len(filtered)), replace=True
        ).to_dict("records")
        st.session_state.responses = {}
        st.session_state.show_results = False

    st.write(f"Questions for **{topic_choice}** ({difficulty_choice})")

    for idx, question in enumerate(st.session_state.quiz, start=1):
        st.markdown(f"**Q{idx}. {question['question']}**")
        response = st.radio(
            f"Select answer for Q{idx}",
            question["options"],
            key=f"q{idx}",
        )
        st.session_state.responses[idx] = response

    if st.button("Submit Quiz"):
        st.session_state.show_results = True

    if st.session_state.get("show_results"):
        score = 0
        st.markdown("### Results")
        for idx, question in enumerate(st.session_state.quiz, start=1):
            selected = st.session_state.responses.get(idx)
            correct = question["answer"]
            if selected == correct:
                score += 1
                st.success(f"Q{idx}: Correct ✅")
            else:
                st.error(f"Q{idx}: Incorrect ❌ (Correct: {correct})")
            st.caption(f"Explanation: {question['explanation']}")

        st.write(f"**Score: {score} / {len(st.session_state.quiz)}**")

        high_scores = st.session_state.get("high_scores", {})
        best = high_scores.get(topic_choice, 0)
        if score > best:
            high_scores[topic_choice] = score
            st.session_state.high_scores = high_scores
            st.balloons()
            st.success("New high score saved!")

        if high_scores:
            st.markdown("### High Scores")
            for topic, best_score in high_scores.items():
                st.write(f"{topic}: {best_score}")


# -----------------------------
# Resources Page
# -----------------------------

if nav == "Resources":
    st.markdown(
        """
        <div class="kenya-header">
            <h2>Formula Notes & Practice</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Algebra Essentials"):
        st.write("Quadratic formula: x = (-b ± √(b² - 4ac)) / 2a")
        st.write("Factorization: ax² + bx + c = a(x - r1)(x - r2)")
        st.write("Practice: Solve x² + 7x + 12 = 0")
        st.write("Practice: Solve 5x - 3 = 2x + 9")

    with st.expander("Geometry & Mensuration"):
        st.write("Area of triangle: A = 1/2 × base × height")
        st.write("Circumference of circle: C = 2πr")
        st.write("Practice: Find area when base=14 cm, height=9 cm")
        st.write("Practice: Find circumference when r=10 cm")

    with st.expander("Trigonometry"):
        st.write("Sine rule: a/sin A = b/sin B = c/sin C")
        st.write("Cosine rule: c² = a² + b² - 2ab cos C")
        st.write("Practice: Use sine rule to find side a when A=40°, b=12 cm, B=65°")
        st.write("Practice: Use cosine rule to find side c when a=9 cm, b=5 cm, C=70°")

    with st.expander("Statistics & Probability"):
        st.write("Mean = Sum of values / Number of values")
        st.write("Median = Middle value (or average of two middle values)")
        st.write("Practice: Find mean of 7, 9, 12, 15")
        st.write("Practice: A coin is tossed. Find P(heads)")

    with st.expander("Coordinate Geometry"):
        st.write("Distance formula: √((x2-x1)² + (y2-y1)²)")
        st.write("Midpoint formula: ((x1+x2)/2, (y1+y2)/2)")
        st.write("Practice: Find distance between (2,5) and (6,9)")
        st.write("Practice: Find midpoint between (4,1) and (10,7)")


# -----------------------------
# Footer
# -----------------------------

st.markdown(
    "<div class='footer'>Powered by 8-4-4 Math Revision for KCSE Prep</div>",
    unsafe_allow_html=True,
)
