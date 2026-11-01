import streamlit as st
import modules.rag_engine as rag_engine


def main():
    st.title("🏠 BiofilmAI & SciProAI Platform — Enterprise Suite")
    st.markdown("""
    Welcome to the **SciProAI Platform** — an integrated bio-analytical operating system combining 
    **deterministic Python automation**, **CLSI/ISO statistical validation**, **deep learning biofilm diagnostics**, 
    and **grounded Gemini RAG intelligence**.
    """)

    st.markdown("---")

    # Platform Feature Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Suite Modules", "8 Modules", delta="100% Unified")
    m2.metric("RAG Engine Status", "Active", delta="PDF Grounded")
    m3.metric("AI Advisor Model", "Gemini 1.5 Flash", delta="Grounded")
    m4.metric("CLSI / ISO Standards", "EP17, EP05, EP09", delta="Compliant")

    st.markdown("---")

    st.markdown("### 🏢 Platform Suite Architecture")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🧪 Commercial & Clinical Quality Suites
        * **🏢 QA/QC Audit Checker (`qcai`)**: Automated evaluation of multi-rule Westgard control runs, %CV intermediate precision, and analytical batch validation.
        * **📄 SOP Compliance Auditor (`sopai`)**: Real-time parsing of laboratory operating procedures, version control audits, and CLSI regulatory checking.
        * **📈 Method Validation Suite (`methodai`)**: CLSI EP17 detection limits (LoB/LoD/LoQ), EP05 precision, EP09 interlab comparability, and standard curve linearity.
        * **📊 Analytics & Dashboards (`dashboards_visualization`)**: Interactive Levey-Jennings charts, polymicrobial growth kinetics, and matrix diffusion heatmaps.
        """)
    with col2:
        st.markdown("""
        #### 🔬 Research & Biofilm Intelligence Suites
        * **🔬 Biofilm NN Diagnostics (`biofilmnn_diagnostics`)**: Deep-learning feature extraction for CLSM/SEM images, surface roughness ($R_a$), and structural viability classification.
        * **🧬 Assay AI Designer (`assayai_design`)**: Molecular assay prototyping, primer/probe melting temperature ($T_m$) scoring, and PCR copy number estimation.
        * **🧫 Biocontrol & AST Suite (`biocontrol_inhibition`)**: Broth microdilution MIC/MBC calculations, zone of inhibition profiling, and FIC synergy indexing.
        * **🧫 BiofilmAI Multimodal (`biofilmai_multimodal`)**: Spatial FISH fluorescence integration, transcriptomic operon expression, and AMR genotype-to-phenotype modeling.
        """)

    st.markdown("---")

    # Grounded Platform-Wide RAG Query
    st.markdown("### 🔍 Grounded Platform Knowledge RAG Search")
    st.write("Query across active laboratory SOPs, validation manuals, and platform documentation:")

    default_home_text = """
    SciProAI Platform Knowledge Base Summary:
    1. Compliance Architecture: Multi-tier RAG engine parsing uploaded PDF SOPs with domain-specific Gemini evaluation.
    2. Statistical Quality Controls: Westgard 1-2s (warning), 1-3s (rejection), R-4s, 4-1s rules enforced across batch runs.
    3. Method Validation Standards: CLSI EP17 Limit of Detection, EP05 Precision Evaluation, and EP09 Method Comparison.
    4. Biofilm Microscopic Thresholds: SYTO 9 / PI live-dead discrimination with roughness coefficient Ra > 0.45 indicating mature matrix.
    """

    query = st.text_input(
        "Ask any laboratory compliance, validation, or biofilm diagnostic question:",
        placeholder="e.g., How does the platform calculate Limit of Detection (LOD) and handle Westgard rule violations?"
    )

    if st.button("Run Platform RAG Search", type="primary", use_container_width=True):
        if query.strip():
            with st.spinner("Searching platform knowledge base..."):
                context = rag_engine.retrieve_relevant_context(query, default_home_text)
                result = rag_engine.query_rag_engine(query, context, "Platform Systems Architect")
                st.success(result)
                with st.expander("🔍 View Retrieved Platform Knowledge Context"):
                    st.code(context, language="text")
        else:
            st.warning("Please enter a query above.")


if __name__ == "__main__":
    main()
