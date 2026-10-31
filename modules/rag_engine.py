import os
import PyPDF2
import streamlit as st

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


def extract_text_from_pdf(file_stream) -> str:
    """Extracts raw text content from uploaded PDF files."""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        return f"Error extracting text: {e}"


def retrieve_relevant_context(query: str, text_content: str, chunk_size: int = 600, top_k: int = 3) -> str:
    """Splits document text into chunks and returns top matching snippets."""
    chunks = [text_content[i : i + chunk_size] for i in range(0, len(text_content), chunk_size)]
    query_words = set(query.lower().split())

    scored_chunks = []
    for chunk in chunks:
        score = sum(1 for word in query_words if word in chunk.lower())
        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for score, chunk in scored_chunks[:top_k]]

    if top_chunks:
        return "\n\n--- [RETRIEVED CONTEXT] ---\n\n".join(top_chunks)
    return text_content[:1800]


def get_available_gemini_model() -> str:
    """Dynamically auto-discovers an active Gemini model supported by your API key."""
    fallback_model = "gemini-1.5-flash"
    try:
        models = list(genai.list_models())
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                clean_name = m.name.replace("models/", "")
                if "flash" in clean_name or "pro" in clean_name:
                    return clean_name
    except Exception:
        pass
    return fallback_model


def query_rag_engine(query: str, context: str, domain_role: str) -> str:
    """Executes Gemini query grounded strictly in retrieved context using dynamic model selection."""
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

    if HAS_GENAI and api_key:
        try:
            genai.configure(api_key=api_key)
            model_name = get_available_gemini_model()
            model = genai.GenerativeModel(model_name)

            prompt = f"""You are an expert {domain_role}.
Answer the user query strictly using the retrieved context provided below. Cite specific sections, numbers, or rules where applicable.

User Query: {query}

Retrieved Context:
{context}"""
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            return f"⚠️ Gemini RAG Execution Error: {e}"

    return (
        f"📄 **Simulated RAG Analysis ({domain_role}):**\n"
        f"- Query processed: '{query}'.\n"
        f"- Retrieved relevant knowledge chunks grounded in uploaded documents."
    )
Click Commit changes....
Step 2: Replace modules/agent_assistant.py on GitHub
Open modules/agent_assistant.py.
Click the Pencil (Edit) icon.
Select all existing text and delete it.
Copy and paste this clean code:
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
            genai.configure(api_key=api_key)
            tools_list = [
                rag_qa_qc_tool,
                rag_method_performance_tool,
                rag_sop_compliance_tool,
                rag_biofilm_diagnostics_tool,
            ]

            model_name = rag_engine.get_available_gemini_model()

            try:
                model = genai.GenerativeModel(model_name=model_name, tools=tools_list)
                chat = model.start_chat(enable_automatic_function_calling=True)
                st.write(f"🛠️ **Step 2: Auto-connected via endpoint `{model_name}`...**")
                response = chat.send_message(user_query)

                st.write("🧪 **Step 3: Synthesizing multi-module intelligence report...**")
                status.update(
                    label="✅ Live Multi-Module Agentic RAG Complete!",
                    state="complete",
                    expanded=False,
                )
                return response.text
            except Exception as err:
                st.warning(f"Gemini Tool Execution error on `{model_name}`: {err}")

        # Fallback Local Keyword Execution Trace
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
