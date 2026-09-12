import streamlit as st

def main():
    st.title("🏠 Welcome to SciProAI")
    st.write("Your precision suite for commercial laboratory QA/QC, assay validation, SOP compliance, and biofilm analytics.")

    # --- Styled Container ---
    with st.container():
        st.markdown("""
        <div style="
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            background-color: #fafafa;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        ">
            <h3 style="margin-bottom: 5px;">🧪 SciProAI Guide</h3>
            <p style="margin-top: 0px; color: #555;">
                Ask a question — I will guide you to the correct commercial tool or research module.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Chatbot UI ---
    user_question = st.text_input(
        "Type your question:",
        placeholder="Example: How do I check QC log outliers? • Validate PCR data • Audit my SOP..."
    )

    ask_button = st.button("Ask", use_container_width=True)

    if ask_button:
        if not user_question.strip():
            st.warning("Please enter a question.")
            return

        q = user_question.lower()

        # --- MODULE ROUTING LOGIC (Updated to 3 Core Tools + Research) ---
        if any(word in q for word in ["qc", "audit", "log", "outlier", "control", "non-conformance"]):
            st.success("Use **🏢 1. QA/QC Log & Audit Checker** → Track instrument logs and flag outliers.")
            return

        if any(word in q for word in ["validation", "assay", "pcr", "qpcr", "ddpr", "formatter", "lod", "loq", "standard curve"]):
            st.success("Use **🏢 2. Assay Data Formatter & Validator** → Clean raw exports and calculate baseline metrics.")
            return

        if any(word in q for word in ["sop", "version", "document", "compliance", "iso", "cross-reference"]):
            st.success("Use **🏢 3. SOP Version Control & Auditor** → Audit Standard Operating Procedures against guidelines.")
            return

        if any(word in q for word in ["biofilm", "gene", "expression", "volcano", "gse", "diagnostics", "inhibition", "assay design"]):
            st.success("Use one of the **🔬 Research Modules** in the sidebar for biofilm analytics and assay design.")
            return

        # --- SIMPLE CONCEPT EXPLANATIONS ---
        if "lod" in q:
            st.info("LoD (Limit of Detection) is the lowest amount of analyte your method can reliably detect.")
            return

        if "volcano" in q:
            st.info("A volcano plot shows gene expression changes: fold change on the x-axis, significance on the y-axis.")
            return

        if "iso" in q:
            st.info("ISO standards define international criteria for quality management and laboratory competence.")
            return

        # --- DEFAULT FALLBACK ---
        st.info("I’m not sure yet — try asking about QC logs, assay validation, SOP auditing, or biofilm analytics.")
