import os
import streamlit as st

# Import platform shared RAG engine
try:
    from modules import rag_engine
except ImportError:
    import rag_engine


def main():
    st.title("📋 SOP Version Control & Compliance Auditor")
    st.markdown("""
    Upload custom **Standard Operating Procedures (PDFs)** or choose default CLIA/ISO guidelines. 
    The grounded RAG engine extracts procedural rules, audits compliance, and highlights revision points.
    """)
    st.markdown("---")

    # Sidebar Document Intake (Preserved from original code)
    st.sidebar.header("📁 Document Intake")
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload Custom SOP (PDF)", 
        type=["pdf"], 
        help="Upload lab manuals, equipment protocols, or CAPA procedures."
    )

    default_sop_text = """
    CLIA Section 4.2 Quality Control Policy:
    1. Any 1_3s Westgard rule failure requires immediate suspension of clinical sample testing.
    2. The operator must recalibrate the optical sensor array and rerun control Lot #204.
    3. Document all corrective actions in the digital CAPA log before resuming patient testing.
    4. ISO 17025 Section 5.4: Instrument recalibrations must be signed off by a certified Lab Quality Manager within 24 hours.
    """

    sop_text = ""
    if uploaded_pdf is not None:
        st.success(f"📄 Custom SOP Uploaded: **{uploaded_pdf.name}**")
        if hasattr(rag_engine, "extract_text_from_pdf"):
            extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        else:
            extracted = "Error extracting text."
            
        if "Error" not in extracted:
            sop_text = extracted
            st.info(f"Successfully extracted {len(sop_text)} characters from **{uploaded_pdf.name}**.")
        else:
            st.error(extracted)
            sop_text = default_sop_text
    else:
        st.info("ℹ️ Using default embedded **CLIA/ISO Laboratory SOP Manual** (Upload a PDF in the sidebar to test custom documents).")
        sop_text = default_sop_text

    # Preview SOP Context Expander (Preserved from original code)
    with st.expander("📖 Preview Extracted SOP Knowledge Base"):
        st.text_area("Active SOP Text Content:", value=sop_text[:2000], height=200, disabled=True)

    st.markdown("### 🔍 Interactive SOP Compliance Audit")
    
    query = st.text_input(
        "Ask a regulatory or compliance query:",
        placeholder="e.g., What are the required actions when a 1_3s Westgard failure occurs?"
    )

    if st.button("🔬 Run SOP Audit Query", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a compliance query above.")
        else:
            # 1. 🤖 Animated Reasoning Status Container (st.status)
            with st.status("📜 Analyzing SOP Rules & Regulatory Framework...", expanded=True) as status:
                try:
                    st.write("🔍 **Step 1: Inspecting SOP knowledge base & retrieving context...**")
                    if hasattr(rag_engine, "retrieve_relevant_context"):
                        retrieved_context = rag_engine.retrieve_relevant_context(query, sop_text)
                    else:
                        retrieved_context = sop_text

                    st.write("⚖️ **Step 2: Synthesizing CLIA/ISO audit findings & CAPA rules...**")
                    if hasattr(rag_engine, "query_rag_engine"):
                        audit_result = rag_engine.query_rag_engine(
                            query=query, 
                            context=retrieved_context, 
                            domain_role="CLIA/ISO Compliance Auditor"
                        )
                    else:
                        audit_result = f"Grounded Context Snippets:\n\n{retrieved_context}"

                    status.update(
                        label="✅ SOP Regulatory Evaluation & Compliance Audit Complete!",
                        state="complete",
                        expanded=False
                    )

                    # 2. 📊 Visual Metric Cards Row (st.metric)
                    st.markdown("### 📊 Audit Status & Document Metrics")
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric(
                            label="Document Source",
                            value="Uploaded PDF" if uploaded_pdf else "CLIA/ISO Manual",
                            delta=uploaded_pdf.name if uploaded_pdf else "Embedded Default",
                            delta_color="normal"
                        )
                    with m2:
                        st.metric(
                            label="Regulatory Standard",
                            value="CLIA / ISO 17025",
                            delta="Verified SOP Rules",
                            delta_color="normal"
                        )
                    with m3:
                        st.metric(
                            label="Audit Readiness",
                            value="Complete",
                            delta="Report Export Ready",
                            delta_color="normal"
                        )

                    # 3. Output Display
                    st.markdown("#### 📑 Compliance Audit Findings")
                    st.success(audit_result)

                    with st.expander("🔍 View Retrieved SOP Context Snippets"):
                        st.code(retrieved_context, language="text")

                    # 4. 📥 1-Click Export Button (st.download_button)
                    st.download_button(
                        label="📥 Export SOP Audit Findings (TXT)",
                        data=f"SOP Document Source: {uploaded_pdf.name if uploaded_pdf else 'CLIA/ISO Default'}\nCompliance Query: {query}\n\nCompliance Audit Findings:\n{audit_result}\n\nRetrieved SOP Context:\n{retrieved_context}",
                        file_name="sciproai_sop_audit_findings.txt",
                        mime="text/plain",
                        help="Click to save a local copy of this SOP compliance evaluation.",
                        use_container_width=True
                    )

                except Exception as e:
                    status.update(label="❌ Audit Analysis Execution Error", state="error")
                    st.error(f"Execution Error: {e}")


if __name__ == "__main__":
    main()
