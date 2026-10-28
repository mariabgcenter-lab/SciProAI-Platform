import os
import streamlit as st

try:
  import google.generativeai as genai

  HAS_GENAI = True
except ImportError:
  HAS_GENAI = False


# ---------------------------------------------------------
# 1. Laboratory Tools (Functions & Schemas)
# ---------------------------------------------------------
def analyze_qa_qc_log(query: str) -> str:
  """Use this tool when asking about Quality Control (QC) runs, Westgard rules, out-of-bound errors, or QA logs."""
  return (
      "📊 **QA/QC Log Analysis:**\n"
      "- **Status:** Flagged Lot #204 (1_3s Westgard rule violation detected on"
      " 2026-10-25).\n"
      "- **Control Value:** 12.4 (Expected range: 10.0 ± 0.8).\n"
      "- **Action Required:** Re-calibrate optical sensor and re-run controls"
      " prior to sample testing."
  )


def evaluate_method_performance(query: str) -> str:
  """Use this tool when asking about method validation, assay precision (%CV), accuracy, or linearity (R2)."""
  return (
      "🔬 **Method Performance Evaluation:**\n"
      "- **Intra-assay Precision (%CV):** 3.2% (Pass target: < 5.0%).\n"
      "- **Linearity (R²):** 0.998 across dynamic range (10^2 to 10^7"
      " copies/µL).\n"
      "- **Action Required:** Assay parameters satisfy CLIA '88 / ISO 17025"
      " verification guidelines."
  )


# ---------------------------------------------------------
# 2. Agentic Reasoning Loop (ReAct + Gemini Tool Calling)
# ---------------------------------------------------------
def run_agentic_reasoning(user_query: str) -> str:
  # Safely read key from Streamlit Secrets or Environment Variable
  api_key = st.secrets.get(
      "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")
  )

  with st.status("🤖 Agent Orchestrator Reasoning...", expanded=True) as status:
    st.write("🔍 **Step 1: Inspecting query intent & selecting tools...**")

    if HAS_GENAI and api_key:
      try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            tools=[analyze_qa_qc_log, evaluate_method_performance],
        )

        chat = model.start_chat(enable_automatic_function_calling=True)
        st.write("🛠️ **Step 2: Executing native LLM function call...**")
        response = chat.send_message(user_query)

        st.write("🧪 **Step 3: Synthesizing final report...**")
        status.update(
            label="✅ Live Gemini Agentic Reasoning Complete!",
            state="complete",
            expanded=False,
        )
        return response.text

      except Exception as e:
        st.warning(f"API execution fallback: {e}")

    # Fallback Execution Trace (Local Keyword Router)
    st.write("🛠️ **Step 2: Executing local module functions...**")
    query_lower = user_query.lower()
    results = []

    if any(
        k in query_lower
        for k in ["qc", "quality control", "westgard", "lot", "log", "flag"]
    ):
      st.write("  ↳ Executing Tool: `analyze_qa_qc_log()`")
      results.append(analyze_qa_qc_log(user_query))

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
      st.write("  ↳ Executing Tool: `evaluate_method_performance()`")
      results.append(evaluate_method_performance(user_query))

    if not results:
      st.write("  ↳ Executing Fallback Multi-Suite Analysis")
      results.append(analyze_qa_qc_log(user_query))
      results.append(evaluate_method_performance(user_query))

    st.write("🧪 **Step 3: Compiling structured output...**")
    status.update(
        label="✅ Agent Workflow Complete!", state="complete", expanded=False
    )
    return "\n\n".join(results)


# ---------------------------------------------------------
# 3. Streamlit Page Render
# ---------------------------------------------------------
def main():
  st.title("🤖 Agentic Lab Assistant (Gemini API Powered)")
  st.markdown("""
    Ask plain-English laboratory questions across your **QA/QC logs** and **Method Performance data**. 
    The AI Agent inspects your request, dynamically calls tool schemas, and synthesizes a unified report.
    """)
  st.markdown("---")

  user_query = st.text_input(
      "Enter your laboratory query:",
      placeholder=(
          "e.g., Check if any QC lots failed yesterday and evaluate our PCR"
          " assay precision."
      ),
  )

  if st.button(
      "Run Agentic AI Analysis", type="primary", use_container_width=True
  ):
    if user_query.strip():
      response = run_agentic_reasoning(user_query)
      st.markdown("### 📋 Agent Intelligence Report")
      st.info(response)
    else:
      st.warning("Please enter a query above before running.")


if __name__ == "__main__":
  main()
