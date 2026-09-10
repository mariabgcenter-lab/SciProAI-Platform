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
# Home Page
# ---------------------------------------------------------
st.title("BG BioWrite Scientific — AI Consulting & Research Suite")

st.write(
    "Welcome to the BG BioWrite Scientific AI Consulting & Research Suite — a unified environment "
    "for laboratory documentation, quality systems, molecular assay optimization, and multimodal biofilm research."
)

st.markdown("---")

# ---------------------------------------------------------
# Overview
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
# Navigation Note
# ---------------------------------------------------------
st.write(
    "Use the navigation menu on the left to open the **Business Suite** or **Research Suite**, "
    "and then select individual modules."
)
