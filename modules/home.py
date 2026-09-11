import streamlit as st

def main():
    st.title("🏠 Welcome to SciProAI")
    st.write("Your assistant for QC, validation, biofilm analytics, training, and documentation.")

    st.subheader("🧪 SciProAI Guide")
    st.write("Ask a question. I’ll guide you or explain simple concepts.")

    # --- Chatbot UI ---
    user_question = st.text_input("Type your question here:")

    if st.button("Ask"):
        if not user_question.strip():
            st.warning("Please enter a question.")
            return

        q = user_question.lower()

        # --- MODULE ROUTING LOGIC ---
        if any(word in q for word in ["validation", "accuracy", "precision", "lod", "loq", "reportable"]):
            st.success("Use **ValidateAI** → Validation Plans & Calculations")
            return

        if any(word in q for word in ["qc", "audit", "controls", "lot", "operator", "quality"]):
            st.success("Use **QCAI** → Quality Control & Audit Suite")
            return

        if any(word in q for word in ["training", "competency", "staff", "qualification"]):
            st.success("Use **TrainAI** → Staff Training & Competency")
            return

        if any(word in q for word in ["sop", "document", "summary", "extract"]):
            st.success("Use **BizDocAI** → Document Summary & Extraction")
            return

        if any(word in q for word in ["biofilm", "gene", "expression", "volcano", "gse"]):
            st.success("Use **BiofilmAI Dashboards** → Gene Expression & Visualization")
            return

        if any(word in q for word in ["workflow", "business", "automation"]):
            st.success("Use **BizAgentAI** → Workflow Automation")
            return

        if any(word in q for word in ["reasoning", "logic", "alignment"]):
            st.success("Use **ReasonAI** → Reasoning Evaluator")
            return

        # --- SIMPLE CONCEPT EXPLANATIONS ---
        if "lod" in q:
            st.info("LoD (Limit of Detection) is the lowest amount of analyte your method can reliably detect.")
            return

        if "volcano" in q:
            st.info("A volcano plot shows gene expression changes: fold change on the x-axis, significance on the y-axis.")
            return

        if "clia" in q:
            st.info("CLIA is a US regulatory framework ensuring laboratory testing quality and accuracy.")
            return

        # --- DEFAULT FALLBACK ---
        st.info("I’m not sure yet — try rephrasing or ask about QC, validation, biofilm, training, SOPs, or workflows.")
