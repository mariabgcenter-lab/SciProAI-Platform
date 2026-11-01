import os
import streamlit as st
import modules.rag_engine as rag_engine

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


# ---------------------------------------------------------
# 1. Multi-Module RAG & Lab Tool Schemas
# ---------------------------------------------------------
def rag_qa_qc_tool(query: str) -> str:
    """Use this tool when asking about QA/QC logs, Westgard violations, control lot histories, or recalibration steps."""
    mock_qc_data = (
        "Lot #204 flagged 2026-10-25 for 1_3s Westgard violation. Control mean 12.4 vs 10.0 target. Action: Recalibrate optical sensor."
    )
    context = rag_engine.retrieve_relevant_context(query, mock_qc_data)
    return rag_engine.query_rag_engine(query, context, "Clinical QA/QC Auditor")


def rag_method_performance_tool(query: str) -> str:
    """Use this tool when asking about assay precision (%CV), linearity (R2), limit of detection (LOD), or method validation."""
    mock_method_data = (
        "Intra-assay precision %CV = 3.2% (Pass target < 5.0%). Linearity R2 = 0.998 across 10^2 to 10^7 copies/uL."
    )
    context = rag_engine.retrieve_relevant_context(query, mock_method_data)
    return rag_engine.query_rag_engine(query, context, "Method Validation Specialist")


def rag_sop_compliance_tool(query: str) -> str:
    """Use this tool when asking about SOP manuals, CLIA '88 / ISO 17025 rules, regulatory policies, or CAPA procedures."""
    mock_sop_data = (
        "CLIA Section 4.2: Westgard 1_3s failure requires immediate testing suspension, sensor recalibration, and CAPA log entry."
    )
    context = rag_engine.retrieve_relevant_context(query, mock_sop_data)
    return rag_engine.query_rag_engine(query, context, "CLIA/ISO Compliance Auditor")


def rag_biofilm_diagnostics_tool(query: str) -> str:
    """Use this tool when asking about BiofilmNN imaging classification, microbial biomass, or microscopy diagnostics."""
    mock_biofilm_data = (
        "BiofilmNN Model: High microbial density detected (Class 3 biofilm). Coverage 78.4%, thickness 42.1 um."
    )
    context = rag_engine.retrieve_relevant_context(query, mock_biofilm_data)
    return rag_engine.query_rag_engine(query, context, "Microbial Diagnostics Specialist")

# ---------------------------------------------------------
# 2. Agentic Reasoning Loop (Multi-Tool Gemini RAG)
# ---------------------------------------------------------
def run_agentic_reasoning(user_query: str) -> str:
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

    with st.status("🤖 Agentic Multi-RAG Orchestrator Reasoning...", expanded=True) as status:
        st.write("🔍 **Step 1: Inspecting query intent across platform RAG tools...**")

        if HAS_GENAI and api_key:
            try:
                genai.configure(api_key=api_key)
                tools_list = [
                    rag_qa_qc_tool,
                    rag_method_performance_tool,
                    rag_sop_compliance_tool,
                    rag_biofilm_diagnostics_tool,
                ]

                candidate_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]

                for model_name in candidate_models:
                    try:
                        model = genai.GenerativeModel(model_name=model_name, tools=tools_list)
                        chat = model.start_chat(enable_automatic_function_calling=True)
                        st.write(f"🛠️ **Step 2: Connected via active endpoint `{model_name}`...**")
                        response = chat.send_message(user_query)

                        st.write("🧪 **Step 3: Synthesizing multi-module intelligence report...**")
                        status.update(
                            label="✅ Live Multi-Module Agentic RAG Complete!",
                            state="complete",
                            expanded=False,
                        )
                        return response.text
                    except Exception:
                        continue
            except Exception:
                pass

        # Fallback Execution Trace
        st.write("🛠️ **Step 2: Running local module RAG evaluations...**")
        results = [
            rag_qa_qc_tool(user_query),
            rag_method_performance_tool(user_query),
            rag_sop_compliance_tool(user_query),
        ]
        status.update(label="✅ Agent Workflow Complete!", state="complete", expanded=False)
        return "\n\n".join(results)

# ---------------------------------------------------------
# 3. Streamlit UI Render
# ---------------------------------------------------------
def main():
    st.title("🤖 Agentic Lab Assistant (Platform-Wide RAG)")
    st.markdown("""
    Ask plain-English laboratory questions across **QA/QC logs**, **Method Statistics**, **SOP Rules**, and **Biofilm Diagnostics**. 
    The AI Agent dynamically queries domain-specific RAG knowledge engines and synthesizes a unified compliance report.
    """)
    st.markdown("---")

    user_query = st.text_input(
        "Enter your query across any module domain:",
        placeholder=(
            "e.g., Did Lot #204 fail, what is our SOP policy for that failure, and check BiofilmNN diagnostics?"
        ),
    )

    if st.button("Run Platform Agentic RAG", type="primary", use_container_width=True):
        if user_query.strip():
            response = run_agentic_reasoning(user_query)
            st.markdown("### 📋 Platform-Wide Agentic RAG Report")
            st.info(response)
        else:
            st.warning("Please enter a query above before running.")


if __name__ == "__main__":
    main()
