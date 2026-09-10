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
# Import Modules (from /modules folder)
# ---------------------------------------------------------
import modules.sopai as sopai
import modules.validateai as validateai
import modules.qcai as qcai
import modules.trainai as trainai
import modules.reasonai as reasonai
import modules.bizdocai as bizdocai
import modules.bizagentai as bizagentai

import modules.biofilmai_multimodal as biofilmai_multimodal
import modules.biofilmnn_diagnostics as biofilmnn_diagnostics
import modules.dashboards_visualization as dashboards_visualization
import modules.biocontrol_inhibition as biocontrol_inhibition
import modules.assayai_design as assayai_design

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
# Routing Logic
# ---------------------------------------------------------
if choice == "🏢 SOPAI":
    sopai.main()
elif choice == "🏢 ValidateAI":
    validateai.main()
elif choice == "🏢 QCAI":
    qcai.main()
elif choice == "🏢 TrainAI":
    trainai.main()
elif choice == "🏢 ReasonAI":
    reasonai.main()
elif choice == "🏢 BizDocAI":
    bizdocai.main()
elif choice == "🏢 BizAgentAI":
    bizagentai.main()
elif choice == "🔬 BiofilmAI Multimodal":
    biofilmai_multimodal.main()
elif choice == "🔬 BiofilmNN Diagnostics":
    biofilmnn_diagnostics.main()
elif choice == "🔬 Dashboards Visualization":
    dashboards_visualization.main()
elif choice == "🔬 Biocontrol Inhibition":
    biocontrol_inhibition.main()
elif choice == "🔬 AssayAI Design":
    assayai_design.main()
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
