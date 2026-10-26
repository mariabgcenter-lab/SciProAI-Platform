import streamlit as st


def analyze_qa_qc_log(query: str) -> str:
  return (
      "📊 **QA/QC Log Analysis:**\n"
      "- Status: Flagged Lot #204 (1_3s Westgard violation detected on"
      " 2026-10-25).\n"
      "- Control Value: 12.4 (Expected range: 10.0 +/- 0.8).\n"
      "- Action Item: Re-calibrate sensor and re-run controls before testing"
      " samples."
  )


def evaluate_method_performance(query: str) -> str:
  return (
      "🔬 **Method Performance Evaluation:**\n"
      "- Intra-assay Precision (%CV): 3.2% (Pass target: < 5.0%).\n"
      "- Linearity (R2): 0.998 across range 10^2 to 10^7 copies/uL.\n"
      "- Action Item: Assay validation parameters meet required clinical QA"
      " targets."
  )


def run_agentic_reasoning(user_query: str) -> str:
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
      "Ask plain-English questions across your QA/QC logs and Method"
      " Performance statistics."
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
