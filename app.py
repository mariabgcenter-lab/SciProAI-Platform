import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BG BioWrite Scientific — AI Consulting Suite",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Home Page — BG BioWrite Scientific
# ---------------------------------------------------------
st.title("BG BioWrite Scientific — AI Consulting Suite")

st.write(
    "Welcome to the BG BioWrite Scientific AI Consulting Suite — a unified professional environment "
    "designed to support SOP creation, CLIA‑aligned documentation, ddPCR/qPCR optimization, QA/QC workflows, "
    "competency development, and AI‑supported laboratory operations."
)

st.markdown("---")

# ---------------------------------------------------------
# About BG BioWrite Scientific
# ---------------------------------------------------------
st.subheader("📘 About BG BioWrite Scientific")

st.write(
    "BG BioWrite Scientific provides professional consulting services including SOP development, "
    "validation planning, molecular assay optimization, biosafety training, quality system support, "
    "and AI‑enhanced scientific documentation for CLIA and research laboratories."
)

st.markdown("---")

# ---------------------------------------------------------
# Available Modules
# ---------------------------------------------------------
st.subheader("🧪 Business AI Modules")

st.markdown("""
### **BG BioWrite Scientific Core Modules**
- **SOP & Protocol Builder** — Generate structured, regulatory‑aligned SOPs  
- **Validation Plan Generator** — Build CLIA‑aligned validation plans  
- **QA/QC Record Assistant** — Create logs, maintenance records, and QC documentation  
- **ddPCR/qPCR Optimization Assistant** — Improve assay sensitivity and reproducibility  
- **Competency & Training Module** — Generate training materials and competency assessments  
- **AI/LLM Biological Reasoning Evaluator** — Assess biological reasoning quality in AI workflows  

### **Scientific Support Modules**
- **Scientific Document Summarization** — Summarize methods, workflows, and publications  
""")

st.markdown("---")

# ---------------------------------------------------------
# Navigation Note
# ---------------------------------------------------------
st.write(
    "Use the navigation menu on the left to explore each module."
)
