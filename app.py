# app.py
import streamlit as st
import sympy as sp
import re
import numpy as np
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────
# Custom CSS with Google Fonts, Bootstrap, Font Awesome
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

# ────────────────────────────────────────────────
# Tabs
# ────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏠 Home", "🔍 Solver", "🤖 AI Help"])

x = sp.symbols('x')

# ─── HOME ───────────────────────────────────────
with tab1:
    st.markdown("<h2>Welcome to MathFun</h2>", unsafe_allow_html=True)
    st.write("""
    This is a revision tool for Kenyan **Form 2** and **Form 3** mathematics under the 8-4-4 system.

    **Current features:**
    • Algebra: equations, inequalities, surds, factorization
    • Graphs: linear, quadratic, systems of equations
    • AI helper: ask any math question and get guidance (powered by OpenAI)

    Select **Solver** to start practicing problems, or **AI Help** for explanations and solutions.
    """)

# ─── SOLVER ─────────────────────────────────────
with tab2:
    st.markdown("<h2><i class='fas fa-tools me-2'></i>Math Solver</h2>", unsafe_allow_html=True)

    section = st.selectbox("Choose topic:", [
        "Algebra – Equations & Inequalities",
        "Algebra – Surds",
        "Algebra – Factorization",
        "Graphs – Quadratic",
        "Graphs – Linear (single)",
        "Graphs – Two lines (intersection)",
        "Graphs – Three lines (system)"
    ])

    st.markdown("---")

    if "Equations & Inequalities" in section:
        st.subheader("Equations & Inequalities")
        st.markdown('<div class="info-box">Examples:<br>• x**2 - 5*x + 6 = 0<br>• 2*x + 3 > 11<br>• x**2 - 4*x + 3 >= 0<br>• 4*x - 12 = 0</div>', unsafe_allow_html=True)

        user_input = st.text_input("Enter equation or inequality:")

        if st.button("Solve", type="primary") and user_input:
            try:
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

                left = sp.sympify(left_str)
                right = sp.sympify(right_str)
                expr = left - right

                if op == '=':
                    if expr.is_polynomial(x) and expr.as_poly(x).degree() == 2:
                        a, b, c = sp.Poly(expr, x).all_coeffs()
                        disc = b**2 - 4*a*c
                        st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                        st.write(f"**Quadratic equation:** {a}x² + {b}x + {c} = 0")
                        st.write(f"Discriminant: D = {disc}")
                        if disc > 0:
                            root1 = (-b + sp.sqrt(disc)) / (2*a)
                            root2 = (-b - sp.sqrt(disc)) / (2*a)
                            st.write(f"Roots: x = {root1}, x = {root2}")
                        elif disc == 0:
                            root = -b / (2*a)
                            st.write(f"Double root: x = {root}")
                        else:
                            st.write("No real roots")
                        st.latex(sp.pretty(sp.solve(expr, x)))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        sol = sp.solve(expr, x)
                        st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                        st.write("**Solution:**")
                        st.latex(sp.pretty(sol))
                        st.markdown('</div>', unsafe_allow_html=True)

                elif op in ['>', '>=', '<', '<=']:
                    rel_map = {'>': sp.StrictGreaterThan, '>=': sp.GreaterThan,
                               '<': sp.StrictLessThan, '<=': sp.LessThan}
                    rel = rel_map[op]
                    solution = sp.solve(rel(left, right), x, domain=sp.S.Reals)

                    st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                    st.write("**Solution set:**")
                    st.latex(sp.pretty(solution))
                    st.write("**Quick steps:**")
                    st.write("1. Find roots of = 0")
                    st.write("2. Test sign in each interval")
                    st.write("3. Include equality if ≥ or ≤")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="error-msg">Error: {str(e)}<br>Tip: Use ** for powers, no spaces around = > <</div>', unsafe_allow_html=True)

    elif "Surds" in section:
        st.subheader("Surds Simplification")
        st.markdown('<div class="info-box">Examples:<br>• sqrt(50)<br>• sqrt(72) - sqrt(18)<br>• 3*sqrt(8) + sqrt(50)</div>', unsafe_allow_html=True)

        surd_input = st.text_input("Enter surd expression:")
        if st.button("Simplify", type="primary") and surd_input:
            try:
                expr = sp.sympify(surd_input)
                simp = sp.simplify(expr)
                st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                st.latex(f"{surd_input} \\quad = \\quad {sp.latex(simp)}")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

    elif "Factorization" in section:
        st.subheader("Factorization")
        st.markdown('<div class="info-box">Examples:<br>• x**2 + 5*x + 6<br>• 2*x**2 - 8*x + 6<br>• x**3 - 8</div>', unsafe_allow_html=True)

        factor_input = st.text_input("Enter polynomial to factor:")
        if st.button("Factor", type="primary") and factor_input:
            try:
                expr = sp.sympify(factor_input)
                factored = sp.factor(expr)
                st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                st.latex(f"{factor_input} \\quad = \\quad {sp.latex(factored)}")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

    elif "Quadratic" in section:
        st.subheader("Quadratic Graph")
        col1, col2, col3 = st.columns(3)
        a = col1.number_input("a", value=1.0)
        b = col2.number_input("b", value=-5.0)
        c = col3.number_input("c", value=6.0)

        if st.button("Plot Quadratic", type="primary"):
            x_vals = np.linspace(-10, 10, 400)
            y_vals = a*x_vals**2 + b*x_vals + c
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.plot(x_vals, y_vals, color='#0d6efd', lw=2.5, label=f'y = {a}x² + {b}x + {c}')
            ax.axhline(0, color='black', lw=0.8)
            ax.axvline(0, color='black', lw=0.8)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

    elif "Linear (single)" in section:
        st.subheader("Single Linear Graph")
        col1, col2 = st.columns(2)
        m = col1.number_input("Slope (m)", value=2.0)
        c = col2.number_input("Intercept (c)", value=-3.0)

        if st.button("Plot", type="primary"):
            x_vals = np.linspace(-10, 10, 400)
            y_vals = m*x_vals + c
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.plot(x_vals, y_vals, color='#198754', lw=2.5, label=f'y = {m}x + {c}')
            ax.axhline(0, color='black', lw=0.8)
            ax.axvline(0, color='black', lw=0.8)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

    elif "Two lines" in section:
        st.subheader("Two Lines – Find Intersection")
        col1, col2, col3, col4 = st.columns(4)
        m1 = col1.number_input("m₁", value=1.0)
        c1 = col2.number_input("c₁", value=2.0)
        m2 = col3.number_input("m₂", value=-2.0)
        c2 = col4.number_input("c₂", value=4.0)

        if st.button("Plot & Solve", type="primary"):
            x_vals = np.linspace(-10, 10, 400)
            y1 = m1*x_vals + c1
            y2 = m2*x_vals + c2
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.plot(x_vals, y1, label=f'y = {m1}x + {c1}', color='#0d6efd')
            ax.plot(x_vals, y2, label=f'y = {m2}x + {c2}', color='#dc3545')

            try:
                sol = sp.solve([m1*x + c1 - (m2*x + c2)], x)
                if sol:
                    xi = float(sol[0])
                    yi = float(m1*xi + c1)
                    ax.plot(xi, yi, 'ko', markersize=10, label=f"({xi:.2f}, {yi:.2f})")
                    st.success(f"Intersection: x = {xi:.3f}, y = {yi:.3f}")
            except:
                st.info("No unique intersection (parallel or coincident)")

            ax.axhline(0, color='black', lw=0.8)
            ax.axvline(0, color='black', lw=0.8)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

    elif "Three lines" in section:
        st.subheader("Three Lines – Check System")
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
            fig, ax = plt.subplots(figsize=(9, 5))
            for i, (m, c) in enumerate(lines):
                y = m*x_vals + c
                ax.plot(x_vals, y, label=f'y = {m}x + {c}', color=colors[i])

            ax.axhline(0, color='black', lw=0.8)
            ax.axvline(0, color='black', lw=0.8)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
            st.info("Look for a common intersection point of all three lines.")

# ─── AI HELP ────────────────────────────────────
with tab3:
    st.markdown("<h2><i class='fas fa-robot me-2'></i>AI Math Helper (OpenAI)</h2>", unsafe_allow_html=True)
    st.write("Ask any Form 2 / Form 3 math question — get step-by-step explanations, hints, or solutions.")

    question = st.text_area(
        "Type your question here:",
        height=160,
        placeholder="Examples:\n"
                    "Solve 3x² - 12x + 9 = 0 step by step\n"
                    "Explain how to calculate bearings in navigation\n"
                    "Help me understand circle theorems with an example\n"
                    "A shop gives 15% discount on a shirt costing 800 KSh. What is the selling price?"
    )

    if st.button("Ask AI", type="primary") and question.strip():
        with st.spinner("Getting answer from AI..."):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # you can change to gpt-4o if you prefer
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly, patient Kenyan math teacher specializing in 8-4-4 O-Level "
                                "Form 2 and Form 3 topics. Explain concepts clearly, step-by-step, using simple "
                                "language suitable for KCSE students. Use LaTeX for math expressions when helpful. "
                                "Show working where appropriate. If the question is unclear, ask for clarification."
                            )
                        },
                        {"role": "user", "content": question}
                    ],
                    temperature=0.65,
                    max_tokens=1400
                )

                answer = response.choices[0].message.content.strip()

                st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                st.markdown("**AI Answer:**")
                st.markdown(answer)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown('<div class="error-msg">', unsafe_allow_html=True)
                st.write("**Error connecting to OpenAI:**")
                st.write(str(e))
                st.write("Please check that OPENAI_API_KEY is correctly set in Streamlit secrets.")
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("MathFun – 8-4-4 F2 & F3 Revision Tool | © 2025")
