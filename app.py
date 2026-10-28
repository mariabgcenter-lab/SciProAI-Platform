# app.py
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BG BioWrite Scientific — Laboratory Automation Suite",
    page_icon="🧬",
    layout="wide",
)

# ---------------------------------------------------------
# Import Core Modules
# ---------------------------------------------------------
import modules.agent_assistant as agent_assistant
import modules.assayai_design as assayai_design
import modules.biocontrol_inhibition as biocontrol_inhibition
import modules.biofilmai_multimodal as biofilmai_multimodal
import modules.biofilmnn_diagnostics as biofilmnn_diagnostics
import modules.dashboards_visualization as dashboards_visualization
import modules.home as home
import modules.methodai as methodai
import modules.qcai as qcai
import modules.sopai as sopai

# ---------------------------------------------------------
# Sidebar Navigation (3 Clean Suites)
# ---------------------------------------------------------
if "nav_choice" not in st.session_state:
  st.session_state.nav_choice = "🏠 Home & Agent Assistant"

st.sidebar.title("SciProAI Navigation")

choice = st.sidebar.radio(
    "Select Suite:",
    [
        "🏠 Home & Agent Assistant",
        "🏢 Compliance & Quality Suite",
        "🔬 Bio-Digital Research Suite",
    ],
    key="nav_choice",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Agentic AI Active:** The Gemini Supervisor agent routes queries"
    " across all modules."
)

# ---------------------------------------------------------
# Suite 1: Home & Agent Assistant
# ---------------------------------------------------------
if choice == "🏠 Home & Agent Assistant":
  tab1, tab2 = st.tabs(["🏠 Platform Overview", "🤖 Agentic Lab Assistant"])
  with tab1:
    home.main()
  with tab2:
    agent_assistant.main()

# ---------------------------------------------------------
# Suite 2: Compliance & Quality Suite
# ---------------------------------------------------------
elif choice == "🏢 Compliance & Quality Suite":
  st.header("🏢 Enterprise Compliance & Quality Suite")
  st.markdown(
      "Automated Westgard rule evaluation, method precision verification, and"
      " CLIA '88 / ISO 17025 SOP compliance auditing."
  )
  st.markdown("---")

  tab1, tab2, tab3 = st.tabs([
      "📊 QA/QC Log & Audit Checker",
      "🔬 Method Performance & Assay Suite",
      "📄 SOP Version Control & Auditor",
  ])

  with tab1:
    qcai.main()
  with tab2:
    methodai.main()
  with tab3:
    sopai.main()

# ---------------------------------------------------------
# Suite 3: Bio-Digital Research Suite
# ---------------------------------------------------------
elif choice == "🔬 Bio-Digital Research Suite":
  st.header("🔬 Bio-Digital Research & Computational Suite")
  st.markdown(
      "Microbial imaging diagnostics, biofilm biomass quantification, and"
      " molecular assay design tools."
  )
  st.markdown("---")

  tab1, tab2, tab3, tab4, tab5 = st.tabs([
      "🧬 AssayAI Design",
      "📷 BiofilmAI Multimodal",
      "🧠 BiofilmNN Diagnostics",
      "📊 Dashboards Visualization",
      "🧫 Biocontrol Inhibition",
  ])

  with tab1:
    assayai_design.main()
  with tab2:
    biofilmai_multimodal.main()
  with tab3:
    biofilmnn_diagnostics.main()
  with tab4:
    dashboards_visualization.main()
  with tab5:
    biocontrol_inhibition.main()
