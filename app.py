# app.py
import streamlit as st
import sympy as sp
from sympy import sympify, solve, simplify, GreaterThan, LessThan, StrictGreaterThan, StrictLessThan
import re
import numpy as np
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────
# Custom CSS: Google Fonts + Bootstrap + Font Awesome + styles
# ────────────────────────────────────────────────
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Open+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <style>
        html, body, [class*="st-"] {
            font-family: 'Open Sans', sans-serif !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 700;
        }
        .stApp {
            background-color: #f8f9fa;
        }
        .main-header {
            color: #1a3c34;
            text-align: center;
            padding: 1.5rem 0;
            background: linear-gradient(135deg, #198754, #0d6efd);
            color: white;
            border-radius: 0 0 15px 15px;
            margin-bottom: 1.5rem;
        }
        .card {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem;
            padding: 1.5rem;
            background: white;
        }
        .stButton > button {
            font-weight: 600;
        }
        .success-msg {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        .error-msg {
            background-color: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="MathFun – 8-4-4 F2 & F3 Math",
    page_icon="📐",
    layout="wide"
)

# ────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────
st.markdown(
    '<div class="main-header"><h1><i class="fas fa-calculator me-2"></i>MathFun</h1>'
    '<p>8-4-4 O-Level Math Revision – Form 2 & Form 3</p></div>',
    unsafe_allow_html=True
)

# ────────────────────────────────────────────────
# Tabs
# ────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Home",
    "🔍 Solver",
    "🧪 Quiz",
    "📚 Resources"
])

# ────────────────────────────────────────────────
# HOME
# ────────────────────────────────────────────────
with tab1:
    st.markdown("<h2>Welcome to MathFun!</h2>", unsafe_allow_html=True)
    st.write("""
    This app helps Kenyan KCSE candidates revise **Form 2** and **Form 3** mathematics topics from the 8-4-4 syllabus.
    
    **Features:**
    - Step-by-step problem solver (equations, inequalities, surds, graphs...)
    - Interactive quizzes with instant feedback (coming soon)
    - Quick formula references
    
    **Start solving now!**
    """)

# ────────────────────────────────────────────────
# SOLVER
# ────────────────────────────────────────────────
with tab2:
    st.markdown("<h2><i class='fas fa-tools me-2'></i>Math Solver</h2>", unsafe_allow_html=True)

    solver_mode = st.radio("Choose solver type:", 
                           ["Equation / Inequality", "Surds Simplification", "Graphical Method"],
                           horizontal=True)

    x = sp.symbols('x')

    if solver_mode == "Equation / Inequality":
        st.subheader("Equation / Inequality Solver")
        st.info("Examples:  \n- x**2 - 5*x + 6 = 0  \n- x**2 - 5*x + 6 > 0  \n- 3*x - 7 <= 11  \n- 2*x**2 + 5*x - 3 = 0")

        user_input = st.text_input("Enter your equation or inequality:")

        if st.button("Solve", type="primary") and user_input:
            try:
                # Clean input: replace ^ with **, remove extra spaces
                cleaned = re.sub(r'\^', '**', user_input.strip())
                cleaned = re.sub(r'\s*([=><]+)\s*', r'\1', cleaned)  # Remove spaces around operators

                # Split on =, >, <, >=, <=
                operators = ['>=', '<=', '>', '<', '=']
                op = None
                for o in operators:
                    if o in cleaned:
                        op = o
                        parts = cleaned.split(o)
                        break

                if op:
                    left_str = parts[0].strip()
                    right_str = parts[1].strip() if len(parts) > 1 else '0'

                    # Convert to SymPy expressions
                    left = sympify(left_str)
                    right = sympify(right_str)

                    expr = left - right  # Bring to form expr = 0 / expr > 0 etc.

                    if op == '=':
                        solution = solve(expr, x)
                        st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                        st.latex(f"\\text{{Solution: }} {sp.pretty(solution)}")
                        st.markdown('</div>', unsafe_allow_html=True)

                    elif op in ['>', '>=', '<', '<=']:
                        if op == '>':
                            rel = StrictGreaterThan
                        elif op == '>=':
                            rel = GreaterThan
                        elif op == '<':
                            rel = StrictLessThan
                        elif op == '<=':
                            rel = LessThan

                        solution = solve(rel(left, right), x, domain=sp.S.Reals)

                        st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                        st.latex(f"\\text{{Solution set: }} {sp.pretty(solution)}")
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.info("**Steps for inequalities (F3 tip):** Find critical points (roots), test intervals, shade where true.")
                    else:
                        st.warning("Unsupported operator. Use =, >, <, >=, <=")
                else:
                    # No operator → treat as expression = 0
                    expr = sympify(cleaned)
                    solution = solve(expr, x)
                    st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                    st.latex(f"\\text{{Solution: }} {sp.pretty(solution)}")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="error-msg">Error: {str(e)}<br>Tip: Use ** for powers (x**2), no spaces around =/>/<, try rephrasing.</div>', unsafe_allow_html=True)

    elif solver_mode == "Surds Simplification":
        st.subheader("Surds Simplifier")
        surd_input = st.text_input("Enter surd expression (e.g. sqrt(50) + 3*sqrt(8) - sqrt(18))")

        if st.button("Simplify", type="primary") and surd_input:
            try:
                expr = sympify(surd_input)
                simplified = simplify(expr)
                st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                st.latex(f"{surd_input} \\quad = \\quad {sp.latex(simplified)}")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-msg">Error: {str(e)}</div>', unsafe_allow_html=True)

    elif solver_mode == "Graphical Method":
        st.subheader("Graphical Solver")
        graph_type = st.selectbox("Plot type:", ["Quadratic", "Inequality Region"])

        if graph_type == "Quadratic":
            col1, col2, col3 = st.columns(3)
            with col1:
                a = st.number_input("a", value=1.0)
            with col2:
                b = st.number_input("b", value=-5.0)
            with col3:
                c = st.number_input("c", value=6.0)

            if st.button("Plot Quadratic", type="primary"):
                x_vals = np.linspace(-10, 10, 400)
                y_vals = a * x_vals**2 + b * x_vals + c

                fig, ax = plt.subplots(figsize=(9, 5))
                ax.plot(x_vals, y_vals, label=f'y = {a}x² + {b}x + {c}', color='#0d6efd', linewidth=2.5)
                ax.axhline(0, color='black', lw=0.8)
                ax.axvline(0, color='black', lw=0.8)
                ax.grid(True, alpha=0.3)
                ax.set_title("Quadratic Graph – Roots at intersections with x-axis")
                ax.legend()
                st.pyplot(fig)

        elif graph_type == "Inequality Region":
            ineq_input = st.text_input("Enter inequality (e.g. x**2 - 4*x + 3 > 0)")

            if st.button("Plot Inequality Region", type="primary") and ineq_input:
                try:
                    cleaned = re.sub(r'\^', '**', ineq_input.strip())
                    expr = sympify(cleaned)

                    func = sp.lambdify(x, expr, 'numpy')
                    x_vals = np.linspace(-10, 10, 800)
                    y_vals = func(x_vals)

                    fig, ax = plt.subplots(figsize=(9, 5))
                    ax.plot(x_vals, y_vals, color='#198754', lw=2.2, label=ineq_input)

                    ax.fill_between(x_vals, y_vals, where=(y_vals > 0), color='green', alpha=0.25, label="True region (>0)")
                    ax.fill_between(x_vals, y_vals, where=(y_vals < 0), color='red', alpha=0.15, label="False region (<0)")

                    ax.axhline(0, color='black', lw=0.8)
                    ax.axvline(0, color='black', lw=0.8)
                    ax.grid(True, alpha=0.3)
                    ax.set_title("Inequality Graphical Solution")
                    ax.legend()
                    st.pyplot(fig)
                except Exception as e:
                    st.markdown(f'<div class="error-msg">Error: {str(e)}</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# QUIZ & RESOURCES (placeholders)
# ────────────────────────────────────────────────
with tab3:
    st.markdown("<h2><i class='fas fa-brain me-2'></i>Quiz</h2>", unsafe_allow_html=True)
    st.info("Quiz feature coming soon – random questions with scoring!")

with tab4:
    st.markdown("<h2><i class='fas fa-book-open me-2'></i>Resources</h2>", unsafe_allow_html=True)
    with st.expander("Quadratic Formula"):
        st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
    with st.expander("Surd Rules"):
        st.write("√(a×b) = √a × √b    |    √(a/b) = √a / √b")
    st.info("More notes & formulas will be added soon!")

st.markdown("---")
st.caption("MathFun – Built for KCSE 8-4-4 F2 & F3 revision | © 2025")
