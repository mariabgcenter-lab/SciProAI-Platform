import streamlit as st

# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------
st.set_page_config(
    page_title="SciProAI — Business Suite",
    layout="wide"
)

st.title("🏢 SciProAI — Business Suite")
st.write("""
Welcome to the **SciProAI Business Suite**, a unified environment for laboratory operations,  
regulatory compliance, SOP generation, QA/QC workflows, competency tracking, and business automation.

Use the sidebar to access each business module:
""")

st.markdown("""
### 📘 Business Modules
- **SOPAI** — Automated SOP & protocol builder  
- **ValidateAI** — Validation plan generator (CLIA, ISO, CAP)  
- **QCAI** — QA/QC record assistant  
- **TrainAI** — Competency & training module  
- **ReasonAI** — LLM reasoning evaluator  
- **BizDocAI** — Business document summary  
- **BizAgentAI** — Business automation agent  
""")

st.markdown("---")

st.write("""
Each module is designed to support laboratory operations, documentation,  
and compliance workflows across clinical, industrial, and research environments.

Select a module from the sidebar to begin.
""")
