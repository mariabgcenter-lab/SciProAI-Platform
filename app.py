import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BG BioWrite Scientific — Laboratory Automation Suite",
    page_icon="🧬",
    layout="wide"
)

# ---------------------------------------------------------
# Import Core Modules (from /modules folder)
# ---------------------------------------------------------
import modules.home as home

# Business Modules
import modules.qcai as qcai                    # 1. QA/QC Log & Audit Checker
import modules.methodai as methodai            # 2. Method Performance, Verification & Assay Suite
import modules.sopai as sopai                  # 3. SOP Version Control & Auditor

# Research Modules
import modules.biofilmai_multimodal as biofilmai_multimodal
import modules.biofilmnn_diagnostics as biofilmnn_diagnostics
import modules.dashboards_visualization as dashboards_visualization
import modules.biocontrol_inhibition as biocontrol_inhibition
import modules.assayai_design as assayai_design

# ---------------------------------------------------------
# Sidebar Navigation (Custom Router with Session State)
# ---------------------------------------------------------
if "nav_choice" not in st.session_state:
    st.session_state.nav_choice = "🏠 Home & Directory"

st.sidebar.title("SciProAI Navigation")

choice = st.sidebar.radio(
    "Select a module:",
    [
        "🏠 Home & Directory",
        "🏢 1. QA/QC Log & Audit Checker",
        "🏢 2. Method Performance & Assay Suite",
        "🏢 3. SOP Version Control & Auditor",
        "🔬 BiofilmAI Multimodal",
        "🔬 BiofilmNN Diagnostics",
        "🔬 Dashboards Visualization",
        "🔬 Biocontrol Inhibition",
        "🔬 AssayAI Design"
    ],
    key="nav_choice"
)

# ---------------------------------------------------------
# Routing Logic — CALL .main() FOR EACH MODULE
# ---------------------------------------------------------
if choice == "🏠 Home & Directory":
    home.main()

elif choice == "🏢 1. QA/QC Log & Audit Checker":
    qcai.main()

elif choice == "🏢 2. Method Performance & Assay Suite":
    methodai.main()

elif choice == "🏢 3. SOP Version Control & Auditor":
    sopai.main()

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
