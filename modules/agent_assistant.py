import streamlit as st


def analyze_qa_qc_log(query: str) -> str:
  """Simulates and analyzes Quality Control logs and Westgard rules."""
  return (
      "📊 **QA/QC Log Analysis:**\n"
      "- **Status:** Flagged Lot #204 (1_3s Westgard violation detected on"
      " 2026-10-25).\n"
      "- **Control Value:** 12.4 (Expected range: 10.0 +/- 0.8).\n"
      "- **Action Item:** Re-calibrate sensor and re-run controls before"
      " testing samples."
  )


def evaluate_method_performance(query: str) -> str:
  """Evaluates method performance metrics like %CV, precision, and linearity."""
  return (
      "🔬 **Method Performance Evaluation:**\n"
      "- **Intra-assay Precision (%CV):** 3.2% (Pass target: < 5.0%).\n"
      "- **Linearity (R2):** 0.998 across range 10^2 to 10^7 copies/uL.\n"
      "- **Action Item:** Assay validation parameters meet required clinical QA"
      " targets."
  )


def run_agentic_reasoning(user_query: str) -> str:
  """Central router that routes queries to the correct lab tool based on context."""
  query_lower = user_query.lower()
  results = []

  qc_keywords = ["qc", "quality control", "westgard", "lot", "log", "flag"]
  method_keywords = [
      "method",
      "performance",
      "cv",
      "precision",
      "accuracy",
      "linearity",
      "validation",
  ]

  if any(k in query_lower for k in qc_keywords):
    results.append(analyze_qa_qc_log(user_query))

  if any(k in query_lower for k in method_keywords):
    results.append(evaluate_method_performance(user_query))

  if not results:
    results.append(analyze_qa_qc_log(user_query))
    results.append(evaluate_method_performance(user_query))

  return "\n\n".join(results)


def main():
  st.title("🤖 Agentic Lab Assistant")
  st.markdown(
      "Ask plain-English questions across your **QA/QC logs** and **Method"
      " Performance statistics**. The AI agent automatically selects the right"
      " evaluation tools and synthesizes an actionable report."
  )
  st.markdown("---")

  user_query = st.text_input(
      "Enter your question or request:",
      placeholder=(
          "e.g., Did any QC lots fail yesterday, and does our assay meet"
          " precision targets?"
      ),
  )

  if st.button(
      "Run AI Assistant Analysis", type="primary", use_container_width=True
  ):
    if user_query.strip():
      with st.spinner("Agent is analyzing request and calling lab tools..."):
        response = run_agentic_reasoning(user_query)
        st.markdown("### 📋 Agent Intelligence Report")
        st.info(response)
    else:
      st.warning("Please enter a query above before running the analysis.")


if __name__ == "__main__":
  main()
Click Commit changes... in the top right.
3. Re-paste Clean Code into app.py
Go back to the main repository folder and click on app.py.
Click the Pencil icon (Edit), select everything, and replace it with this clean routing script:
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
# Import Core Modules (from /modules folder)
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
# Sidebar Navigation (Custom Router with Session State)
# ---------------------------------------------------------
if "nav_choice" not in st.session_state:
  st.session_state.nav_choice = "🏠 Home & Directory"

st.sidebar.title("SciProAI Navigation")

choice = st.sidebar.radio(
    "Select a module:",
    [
        "🏠 Home & Directory",
        "🤖 Agentic Lab Assistant",
        "🏢 1. QA/QC Log & Audit Checker",
        "🏢 2. Method Performance & Assay Suite",
        "🏢 3. SOP Version Control & Auditor",
        "🔬 AssayAI Design",
        "🔬 BiofilmAI Multimodal",
        "🔬 BiofilmNN Diagnostics",
        "🔬 Dashboards Visualization",
        "🔬 Biocontrol Inhibition",
    ],
    key="nav_choice",
)

# ---------------------------------------------------------
# Routing Logic — CALL .main() FOR EACH MODULE
# ---------------------------------------------------------
if choice == "🏠 Home & Directory":
  home.main()

elif choice == "🤖 Agentic Lab Assistant":
  agent_assistant.main()

elif choice == "🏢 1. QA/QC Log & Audit Checker":
  qcai.main()

elif choice == "🏢 2. Method Performance & Assay Suite":
  methodai.main()

elif choice == "🏢 3. SOP Version Control & Auditor":
  sopai.main()

elif choice == "🔬 AssayAI Design":
  assayai_design.main()

elif choice == "🔬 BiofilmAI Multimodal":
  biofilmai_multimodal.main()

elif choice == "🔬 BiofilmNN Diagnostics":
  biofilmnn_diagnostics.main()

elif choice == "🔬 Dashboards Visualization":
  dashboards_visualization.main()

elif choice == "🔬 Biocontrol Inhibition":
  biocontrol_inhibition.main()
