import streamlit as st

def main():
    st.title("🧬 SciProAI Platform Hub & Guide")
    st.markdown("""
    Welcome to **SciProAI**—an enterprise-grade modular platform engineered to streamline commercial molecular laboratory operations, 
    automate QA/QC and SOP compliance, and drive advanced scientific research.
    """)

    st.markdown("---")

    st.subheader("🏢 Commercial Business Modules (Operational Suite)")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📋 QA/QC Auditor (`qcai`)")
        st.write("Audit instrument maintenance logs, batch release records, and environmental monitoring thresholds.")

    with col2:
        st.markdown("### 📈 Method & Assay Suite (`methodai`)")
        st.write("Format instrument data, calculate CLSI EP17 limits (LoB/LoD/LoQ), parse ddPCR droplets, and run method comparisons.")

    with col3:
        st.markdown("### 📄 SOP Compliance (`sopai`)")
        st.write("Manage standard operating procedures, track version histories, and verify document compliance.")

    st.markdown("---")

    st.subheader("🔬 Scientific Research Suites")
    st.info("""
    * **`assayai_design`**: Advanced molecular assay design and primer/probe evaluation suite.
    * **Biofilm & Biocontrol Suites**: Multimodal modeling, neural network diagnostics, interactive visualization dashboards, and inhibition analytics.
    """)

    st.markdown("---")

    # Embedded Platform Guide & Directory
    st.subheader("📖 Complete Platform Architecture & Directory")
    
    st.markdown("### Core Commercial Business Modules")
    st.info("""
    * **`qcai.py` (QA/QC Log & Audit Checker):** Audits instrument maintenance logs, environmental monitoring data, and batch release records against quality control thresholds.
    * **`methodai.py` (Method Performance, Verification & Assay Suite):** Formats raw instrument outputs, calculates quantitative linearity & amplification efficiency, computes CLSI EP17 detection limits (LoB, LoD, LoQ), processes digital PCR (ddPCR) Poisson partitioning, and executes method verification/comparison audits.
    * **`sopai.py` (SOP Version Control & Auditor):** Manages standard operating procedure documentation, tracks version changes, and audits procedural compliance.
    """)
    
    st.markdown("### Scientific Research Modules")
    st.success("""
    * **`biofilmai_multimodal.py`**: Multimodal biofilm modeling and analysis.
    * **`biofilmnn_diagnostics.py`**: Neural network diagnostics for microbial biofilms.
    * **`dashboards_visualization.py`**: Interactive data visualization dashboards.
    * **`biocontrol_inhibition.py`**: Antimicrobial inhibition and biocontrol analytics.
    * **`assayai_design.py`**: Advanced molecular assay design and primer/probe optimization.
    """)

    st.markdown("---")
    st.markdown("*Use the left sidebar navigation to switch directly between operational and research modules.*")
