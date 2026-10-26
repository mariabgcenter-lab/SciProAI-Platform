import re
import streamlit as st


# ==============================================================================
# 1. Define Laboratory Tools & Reasoning Logic
# ==============================================================================
def analyze_qa_qc_log(query: str) -> str:
  """Simulates/analyzes Quality Control logs, Westgard rules, and out-of-spec flags."""
  return (
      "📊 **QA/QC Log Analysis:**\n"
      "- **Status:** Flagged Lot #204 (1_3s Westgard violation detected on"
      " 2026-10-25).\n"
      "- **Control Value:** 12.4 (Expected range: 10.0 ± 0.8).\n"
      "- **Action Item:** Re-calibrate sensor and re-run controls before"
      " testing patient/research samples."
  )


def evaluate_method_performance(query: str) -> str:
  """Evaluates method performance metrics like %CV, precision, accuracy, and linearity."""
  return (
      "🔬 **Method Performance Evaluation:**\n"
      "- **Intra-assay Precision (%CV):** 3.2% (Pass target: < 5.0%).\n"
      "- **Linearity (R²):** 0.998 across range 10^2 to 10^7 copies/µL.\n"
      "- **Action Item:** Assay validation parameters meet required clinical QA"
      " targets."
  )


def run_agentic_reasoning(user_query: str) -> str:
  """Central router that routes the query to the correct tool based on context."""
  query_lower = user_query.lower()
  results = []

  # Route to QA/QC tool if QC keywords detected
  if any(
      k in query_lower
      for k in ["qc", "quality control", "westgard", "lot", "log", "flag"]
  ):
    results.append(analyze_qa_qc_log(user_query))

  # Route to Method Performance tool if method keywords detected
  if any(
      k in query_lower
      for k in [
          "method",
          "performance",
          "cv",
          "precision",
          "accuracy",
          "linearity",
          "validation",
      ]
  ):
    results.append(evaluate_method_performance(user_query))

  # If query is general, invoke both tools
  if not results:
    results.append(analyze_qa_qc_log(user_query))
    results.append(evaluate_method_performance(user_query))

  return "\n\n".join(results)


# ==============================================================================
# 2. Main Page Render Function (Called by app.py)
# ==============================================================================
def main():
  st.title("🤖 Agentic Lab Assistant")
  st.markdown("""
    Ask plain-English questions across your **QA/QC logs** and **Method Performance statistics**. 
    The AI agent automatically selects the right evaluation tools and synthesizes an actionable report.
    """)
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
Step 3: Connect it inside app.py
In your main app.py file, add the module import at the top and include it in your navigation menu:
# 1. At the top of app.py, import the new module:
import modules.agent_assistant as agent_assistant
import modules.sopai as sopai

# 2. In your sidebar navigation selection in app.py:
selected_module = st.sidebar.radio(
    "Select Platform Module:",
    ["SOP Auditor", "QA/QC & Method Agent", "Other Modules..."],
)

# 3. Add the conditional block to run it:
if selected_module == "SOP Auditor":
  sopai.main()
elif selected_module == "QA/QC & Method Agent":
  agent_assistant.main()
  
