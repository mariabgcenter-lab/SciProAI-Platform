import streamlit as st

# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------
st.set_page_config(
    page_title="SciProAI — Research Suite",
    layout="wide"
)

st.title("🔬 SciProAI — Research Suite")
st.write("""
Welcome to the **SciProAI Research Suite**, a unified environment for multimodal biofilm prediction,  
molecular assay optimization, scientific visualization, and experimental design support.

Use the sidebar to access each research module:
""")

st.markdown("""
### 🔬 Research Modules
- **BiofilmAI Multimodal** — multimodal biofilm prediction  
- **BiofilmNN Diagnostics** — neural network diagnostics for biofilm formation  
- **Dashboards Visualization** — scientific dashboards and plots  
- **Biocontrol Inhibition** — inhibition zone analysis and biocontrol modeling  
- **AssayAI Design** — molecular assay optimization and design  
""")

st.markdown("---")

st.write("""
Each module is designed to support scientific analysis, visualization,  
and machine‑learning workflows for microbiology and molecular diagnostics.

Select a module from the sidebar to begin.
""")
