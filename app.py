import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BG BioWrite Scientific — AI Consulting & Research Suite",
    page_icon="🧬",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar Navigation (ALL modules now in /modules)
# ---------------------------------------------------------

st.sidebar.title("🏢 Business Suite")

st.sidebar.page_link("modules/sopai.py", label="SOPAI")
st.sidebar.page_link("modules/validateai.py", label="ValidateAI")
st.sidebar.page_link("modules/qcai.py", label="QCAI")
st.sidebar.page_link("modules/trainai.py", label="TrainAI")
st.sidebar.page_link("modules/reasonai.py", label="ReasonAI")
st.sidebar.page_link("modules/bizdocai.py", label="BizDocAI")
st.sidebar.page_link("modules/bizagentai.py", label="BizAgentAI")

st.sidebar.title("🔬 Research Suite")

st.sidebar.page_link("modules/biofilmai_multimodal.py", label="BiofilmAI Multimodal")
st.sidebar.page_link("modules/biofilmnn_diagnostics.py", label="BiofilmNN Diagnostics")
st.sidebar.page_link("modules/dashboards_visualization.py", label="Dashboards Visualization")
st.sidebar.page_link("modules/biocontrol_inhibition.py", label="Biocontrol Inhibition")
st.sidebar.page_link("modules/assayai_design.py", label="AssayAI Design")

# ---------------------------------------------------------
# Home Page Content
# ---------------------------------------------------------

st.title("BG BioWrite Scientific — AI Consulting & Research Suite")

st.write(
    "Welcome to the BG BioWrite Scientific AI Consulting & Research Suite — a unified environment "
    "for laboratory documentation, quality systems, molecular assay optimization, and multimodal biofilm research."
)

st.markdown("---")

st.subheader("🏁 Suite Overview")

st.markdown("""
This application is organized into two main sections:

### 🧪 Business Suite — BG BioWrite Scientific  
Focused on consulting, documentation, training, and AI‑supported quality systems for CLIA and research laboratories.

### 🔬 Research Suite — BiofilmAI  
Focused on multimodal biofilm prediction, molecular assay optimization, and scientific document support.

Use the sidebar to open modules in either suite.
""")
