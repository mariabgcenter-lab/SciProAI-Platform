import streamlit as st
import modules.rag_engine as rag_engine

def main():
    st.title("📋 SOP Version Control & Compliance Auditor")
    st.markdown("""
    Upload custom **Standard Operating Procedures (PDFs)** or choose default CLIA/ISO guidelines. 
    The grounded RAG engine extracts procedural rules, audits compliance, and highlights revision points.
    """)
    st.markdown("---")

    # Sidebar or Main PDF Uploader
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
        extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        if "Error" not in extracted:
            sop_text = extracted
            st.info(f"Successfully extracted {len(sop_text)} characters from **{uploaded_pdf.name}**.")
        else:
            st.error(extracted)
            sop_text = default_sop_text
    else:
        st.info("ℹ️ Using default embedded **CLIA/ISO Laboratory SOP Manual** (Upload a PDF in the sidebar to test custom documents).")
        sop_text = default_sop_text

    # Preview SOP Context
    with st.expander("📖 Preview Extracted SOP Knowledge Base"):
        st.text_area("Active SOP Text Content:", value=sop_text[:2000], height=200, disabled=True)

    st.markdown("### 🔍 Interactive SOP Compliance Audit")
    
    query = st.text_input(
        "Ask a regulatory or compliance query:",
        placeholder="e.g., What are the required actions when a 1_3s Westgard failure occurs?"
    )

    if st.button("Run SOP Audit Query", type="primary", use_container_width=True):
        if query.strip():
            with st.spinner("Extracting SOP rules and grounding compliance analysis..."):
                retrieved_context = rag_engine.retrieve_relevant_context(query, sop_text)
                audit_result = rag_engine.query_rag_engine(
                    query=query, 
                    context=retrieved_context, 
                    domain_role="CLIA/ISO Compliance Auditor"
                )
                
                st.markdown("#### 📑 Compliance Audit Findings")
                st.success(audit_result)
                
                with st.expander("🔍 View Retrieved SOP Context Snippets"):
                    st.code(retrieved_context, language="text")
        else:
            st.warning("Please enter a compliance query above.")

if __name__ == "__main__":
    main()
