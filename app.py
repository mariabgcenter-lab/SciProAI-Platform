import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BG BioWrite Scientific — AI Consulting & Research Suite",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# Home Page — BG BioWrite Scientific + BiofilmAI
# ---------------------------------------------------------
st.title("BG BioWrite Scientific — AI Consulting & Research Suite")

st.write(
    "Welcome to the BG BioWrite Scientific AI Consulting & Research Suite — a unified environment "
    "for laboratory documentation, quality systems, molecular assay optimization, and multimodal biofilm research."
)

st.markdown("---")

# ---------------------------------------------------------
# High-Level Sections
# ---------------------------------------------------------
st.subheader("🏁 Suite Overview")

st.markdown("""
This application is organized into two main sections:

### 🧪 Business Suite — BG BioWrite Scientific
Focused on consulting, documentation, training, and AI‑supported quality systems for CLIA and research laboratories.

### 🔬 Research Suite — BiofilmAI
Focused on multimodal biofilm prediction, molecular assay optimization, and scientific document support.
""")

st.markdown("---")

# ---------------------------------------------------------
# Business Suite — BG BioWrite Scientific
# ---------------------------------------------------------
st.subheader("🧪 Business Suite — BG BioWrite Scientific")

st.write(
    "The Business Suite provides consulting‑oriented tools for SOPs, validation plans, QA/QC records, "
    "competency development, and AI/LLM reasoning evaluation."
)

st.markdown("""
### Core Business Modules
- **SOP & Protocol Builder** — Generate structured, regulatory‑aligned SOPs  
- **Validation Plan Generator** — Build CLIA‑aligned validation plans  
- **QA/QC Record Assistant** — Create logs, maintenance records, and QC documentation  
- **Competency & Training Module** — Generate training materials and competency assessments  
- **AI/LLM Biological Reasoning Evaluator** — Assess biological reasoning quality in AI workflows  
- **Scientific Document Summarization (Business)** — Summarize methods, workflows, and technical documents for operational use  
""")

st.markdown("---")

# ---------------------------------------------------------
# Research Suite — BiofilmAI
# ---------------------------------------------------------
st.subheader("🔬 Research Suite — BiofilmAI")

st.write(
    "The Research Suite supports multimodal biofilm prediction, molecular assay optimization, and "
    "scientific document interpretation for research workflows."
)

st.markdown("""
### Core Research Modules
- **Gene Expression Checker** — Analyze transcriptomic features used in Project A  
- **Biofilm Image Analyzer** — Process microscopy images used in Project B  
- **Multimodal Fusion Hub** — Preview how gene and image features combine in Project C  
- **ddPCR/qPCR Optimization Assistant** — Improve molecular assay sensitivity and reproducibility  
- **Scientific Document Summarization (Research)** — Summarize scientific documents to extract experimental purpose and context  
- **SOP/Protocol Summary Assistant** — Summarize procedural scientific workflows (SOPs, protocols, JoVE‑style methods)  
""")

st.markdown("---")

# ---------------------------------------------------------
# Navigation Note
# ---------------------------------------------------------
st.write(
    "Use the navigation menu on the left to open the **Business Suite** or **Research Suite** pages, "
    "and then select individual modules from the sidebar."
)
