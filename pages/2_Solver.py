# pages/2_Solver.py
import streamlit as st
from utils.math_solver import solve_equation_inequality, simplify_surds
from utils.graph_utils import plot_quadratic, plot_linear_system

st.header("🔍 Math Solver")

solver_mode = st.radio("Choose type:", 
                       ["Equations & Inequalities", "Surds", "Graphs"],
                       horizontal=True)

if solver_mode == "Equations & Inequalities":
    # your equation/inequality code here
    # or call: solve_equation_inequality(user_input)
    pass

# ... rest of solver logic moved here
