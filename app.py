# app.py
import streamlit as st
import sympy as sp
from sympy import sympify, solve, simplify, GreaterThan, LessThan, StrictGreaterThan, StrictLessThan
import re
import numpy as np
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────
# Custom CSS
# ────────────────────────────────────────────────
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Open+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <style>
        html, body, [class*="st-"] { font-family: 'Open Sans', sans-serif !important; }
        h1, h2, h3, h4, h5, h6 { font-family: 'Nunito', sans-serif !important; font-weight: 700; }
        .stApp { background-color: #f8f9fa; }
        .main-header {
            color: #1a3c34; text-align: center; padding: 1.5rem 0;
            background: linear-gradient(135deg, #198754, #0d6efd); color: white;
            border-radius: 0 0 15px 15px; margin-bottom: 1.5rem;
        }
        .card { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-bottom: 1.5rem; padding: 1.5rem; background: white; }
        .stButton > button { font-weight: 600; }
        .success-msg { background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
        .info-box  { background-color: #e7f3ff; color: #004085; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
        .error-msg { background-color: #f8d7da; color: #721c24; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="MathFun – 8-4-4 F2 & F3", page_icon="📐", layout="wide")

# Header
st.markdown(
    '<div class="main-header"><h1><i class="fas fa-calculator me-2"></i>MathFun</h1>'
    '<p>8-4-4 O-Level Math Revision – Form 2 & Form 3</p></div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Solver", "🧪 Quiz", "📚 Resources"])

# ─── HOME ───────────────────────────────────────
with tab1:
    st.markdown("<h2>Welcome to MathFun!</h2>", unsafe_allow_html=True)
    st.write("""
    Kenyan KCSE revision tool for **Form 2** & **Form 3** 8-4-4 Mathematics.

    **Current features:**
    • Step-by-step equation & inequality solver
    • Surds simplification with steps
    • Graphs: linear (1–3 lines), quadratic, inequality regions
    • More coming soon: quizzes, bearings, probability...

    Select **Solver** to begin!
    """)

# ─── SOLVER ─────────────────────────────────────
with tab2:
    st.markdown("<h2><i class='fas fa-tools me-2'></i>Math Solver</h2>", unsafe_allow_html=True)

    solver_mode = st.radio("Choose type:", 
                           ["Equations & Inequalities", "Surds", "Graphs"],
                           horizontal=True)

    x = sp.symbols('x')

    if solver_mode == "Equations & Inequalities":
        st.subheader("Equation / Inequality Solver")
        st.markdown('<div class="info-box">Examples:<br>• x² - 5x + 6 = 0<br>• 2x + 3 > 11<br>• x² - 4x + 3 ≥ 0<br>• 4x - 12 = 0</div>', unsafe_allow_html=True)

        user_input = st.text_input("Enter equation or inequality:")

        if st.button("Solve", type="primary") and user_input:
            try:
                # Clean input
                cleaned = re.sub(r'\^', '**', user_input.strip())
                cleaned = re.sub(r'\s*([=><]+)\s*', r'\1', cleaned)

                operators = ['>=', '<=', '>', '<', '=']
                op = None
                left_str, right_str = cleaned, "0"

                for o in operators:
                    if o in cleaned:
                        op = o
                        parts = cleaned.split(o, 1)
                        left_str = parts[0].strip()
                        right_str = parts[1].strip() if len(parts) > 1 else "0"
                        break

                left = sympify(left_str)
                right = sympify(right_str)
                expr = left - right

                steps = []

                if op == '=':
                    # ── Quadratic or linear equation ──
                    if expr.is_polynomial(x) and expr.as_poly(x).degree() == 2:
                        a, b, c = sp.Poly(expr, x).all_coeffs()
                        steps.append(f"Quadratic: {a}x² + {b}x + {c} = 0")
                        disc = b**2 - 4*a*c
                        steps.append(f"Discriminant: D = b² - 4ac = {disc}")
                        if disc > 0:
                            root1 = (-b + sp.sqrt(disc)) / (2*a)
                            root2 = (-b - sp.sqrt(disc)) / (2*a)
                            steps.append(f"Roots: x = {root1}, x = {root2}")
                        elif disc == 0:
                            root = -b / (2*a)
                            steps.append(f"Double root: x = {root}")
                        else:
                            steps.append("No real roots")
                    else:
                        sol = solve(expr, x)
                        steps.append(f"Solution: {sol}")

                    st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                    for step in steps:
                        st.write(step)
                    st.latex(sp.pretty(solve(expr, x)))
                    st.markdown('</div>', unsafe_allow_html=True)

                elif op in ['>', '>=', '<', '<=']:
                    rel_map = {'>': StrictGreaterThan, '>=': GreaterThan,
                               '<': StrictLessThan,  '<=': LessThan}
                    rel = rel_map[op]

                    solution = solve(rel(left, right), x, domain=sp.S.Reals)

                    st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                    st.write("**Solution set:**")
                    st.latex(sp.pretty(solution))
                    st.write("**Steps (F3 tip):**")
                    st.write("1. Solve = 0 to find critical points")
                    st.write("2. Test sign in each interval")
                    st.write("3. Include equality points if ≥ or ≤")
                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.warning("Use =, >, <, >=, <=")

            except Exception as e:
                st.markdown(f'<div class="error-msg">Error: {str(e)}<br>Tip: Use ** for powers, no spaces around operators.</div>', unsafe_allow_html=True)

    elif solver_mode == "Surds":
        st.subheader("Surds Simplifier")
        st.markdown('<div class="info-box">Examples:<br>• sqrt(50)<br>• sqrt(72) - sqrt(18)<br>• 3*sqrt(8) + sqrt(50)</div>', unsafe_allow_html=True)

        surd_input = st.text_input("Enter surd expression:")

        if st.button("Simplify", type="primary") and surd_input:
            try:
                expr = sympify(surd_input)
                simp = simplify(expr)

                steps = [f"Original: {surd_input}"]
                if expr != simp:
                    steps.append(f"Simplified: {simp}")

                st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                for s in steps:
                    st.write(s)
                st.latex(sp.latex(simp))
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="error-msg">Error: {str(e)}</div>', unsafe_allow_html=True)

    elif solver_mode == "Graphs":
        st.subheader("Graphical Solver")
        graph_type = st.selectbox("Plot type:", ["Quadratic", "Linear (one line)", "Two lines (intersection)", "Three lines (system)"])

        fig, ax = plt.subplots(figsize=(9, 5.5))

        if graph_type == "Quadratic":
            col1, col2, col3 = st.columns(3)
            a = col1.number_input("a", value=1.0)
            b = col2.number_input("b", value=-5.0)
            c = col3.number_input("c", value=6.0)

            if st.button("Plot", type="primary"):
                x_vals = np.linspace(-10, 10, 400)
                y_vals = a*x_vals**2 + b*x_vals + c
                ax.plot(x_vals, y_vals, color='#0d6efd', lw=2.5, label=f'y = {a}x² + {b}x + {c}')
                ax.set_title("Quadratic Graph")

        elif graph_type == "Linear (one line)":
            col1, col2 = st.columns(2)
            m = col1.number_input("Slope (m)", value=2.0)
            c = col2.number_input("Y-intercept (c)", value=-3.0)

            if st.button("Plot", type="primary"):
                x_vals = np.linspace(-10, 10, 400)
                y_vals = m*x_vals + c
                ax.plot(x_vals, y_vals, color='#198754', lw=2.5, label=f'y = {m}x + {c}')
                ax.set_title("Linear Graph")

        elif graph_type == "Two lines (intersection)":
            st.write("Enter two lines: y = m₁x + c₁ and y = m₂x + c₂")
            col1, col2, col3, col4 = st.columns(4)
            m1 = col1.number_input("m₁", value=1.0)
            c1 = col2.number_input("c₁", value=2.0)
            m2 = col3.number_input("m₂", value=-2.0)
            c2 = col4.number_input("c₂", value=4.0)

            if st.button("Plot & Find Intersection", type="primary"):
                x_vals = np.linspace(-10, 10, 400)
                y1 = m1*x_vals + c1
                y2 = m2*x_vals + c2
                ax.plot(x_vals, y1, label=f'y = {m1}x + {c1}', color='#0d6efd')
                ax.plot(x_vals, y2, label=f'y = {m2}x + {c2}', color='#dc3545')

                # Find intersection
                try:
                    sol = solve([m1*x + c1 - (m2*x + c2)], x)
                    if sol:
                        xi = float(sol[0])
                        yi = float(m1*xi + c1)
                        ax.plot(xi, yi, 'ko', markersize=10, label=f"Intersection ({xi:.2f}, {yi:.2f})")
                        st.success(f"Intersection at x = {xi:.3f}, y = {yi:.3f}")
                except:
                    st.info("No unique intersection (parallel or same line)")

                ax.set_title("Two Linear Equations")

        elif graph_type == "Three lines (system)":
            st.write("Enter three lines (checks consistency of 3 equations)")
            cols = st.columns(3)
            lines = []
            colors = ['#0d6efd', '#dc3545', '#ffc107']
            for i in range(3):
                with cols[i]:
                    m = st.number_input(f"m{i+1}", value=float(1 - i*1.5), key=f"m{i}")
                    c = st.number_input(f"c{i+1}", value=float(2 + i*2), key=f"c{i}")
                    lines.append((m, c))

            if st.button("Plot", type="primary"):
                x_vals = np.linspace(-10, 10, 400)
                for i, (m, c) in enumerate(lines):
                    y = m*x_vals + c
                    ax.plot(x_vals, y, label=f'y = {m}x + {c}', color=colors[i])

                ax.set_title("Three Linear Equations – Check for common point")

                st.info("For 3 lines to have one solution they must intersect at **one common point**.\nParallel or inconsistent = no solution / infinite solutions.")

        # Common plot settings
        ax.axhline(0, color='black', lw=0.8)
        ax.axvline(0, color='black', lw=0.8)
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)

# ─── QUIZ & RESOURCES (placeholders) ────────────
with tab3:
    st.markdown("<h2><i class='fas fa-brain me-2'></i>Quiz</h2>", unsafe_allow_html=True)
    st.info("Quizzes coming soon — topic-based questions with scoring!")

with tab4:
    st.markdown("<h2><i class='fas fa-book-open me-2'></i>Resources</h2>", unsafe_allow_html=True)
    with st.expander("Quadratic Formula"):
        st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
    with st.expander("Linear Equation (y = mx + c)"):
        st.write("m = slope, c = y-intercept")
    with st.expander("Surd Rules"):
        st.write("√(a×b) = √a × √b    |    √(a/b) = √a / √b")
    st.info("More notes coming soon!")

st.markdown("---")
st.caption("MathFun – KCSE 8-4-4 F2 & F3 Revision Tool | © 2025")
