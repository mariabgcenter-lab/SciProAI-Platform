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
# Sidebar Navigation (Custom Router)
# ---------------------------------------------------------
st.sidebar.title("SciProAI Navigation")

choice = st.sidebar.radio(
    "Select a module:",
    [
        "🏢 SOPAI",
        "🏢 ValidateAI",
        "🏢 QCAI",
        "🏢 TrainAI",
        "🏢 ReasonAI",
        "🏢 BizDocAI",
        "🏢 BizAgentAI",
        "🔬 BiofilmAI Multimodal",
        "🔬 BiofilmNN Diagnostics",
        "🔬 Dashboards Visualization",
        "🔬 Biocontrol Inhibition",
        "🔬 AssayAI Design"
    ]
)

# ---------------------------------------------------------
# Routing Logic (NO .main() calls — modules run automatically)
# ---------------------------------------------------------
if choice == "🏢 SOPAI":
    import modules.sopai

elif choice == "🏢 ValidateAI":
    import modules.validateai

elif choice == "🏢 QCAI":
    import modules.qcai

elif choice == "🏢 TrainAI":
    import modules.trainai

elif choice == "🏢 ReasonAI":
    import modules.reasonai

elif choice == "🏢 BizDocAI":
    import modules.bizdocai

elif choice == "🏢 BizAgentAI":
    import modules.bizagentai

elif choice == "🔬 BiofilmAI Multimodal":
    import modules.biofilmai_multimodal

elif choice == "🔬 BiofilmNN Diagnostics":
    import modules.biofilmnn_diagnostics

elif choice == "🔬 Dashboards Visualization":
    import modules.dashboards_visualization

elif choice == "🔬 Biocontrol Inhibition":
    import modules.biocontrol_inhibition

elif choice == "🔬 AssayAI Design":
    import modules.assayai_design

# ---------------------------------------------------------
# Default Landing Page
# ---------------------------------------------------------
else:
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
