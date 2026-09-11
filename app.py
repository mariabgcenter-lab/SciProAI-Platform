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
import modules.home as home
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
        "🏠 Home",
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
# Routing Logic — CALL .main() FOR EACH MODULE
# ---------------------------------------------------------
if choice == "🏠 Home":
    home.main()

elif choice == "🏢 SOPAI":
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
