import streamlit as st

def main():
    st.title("🧬 SciProAI Platform Hub & Guide")
    st.markdown("""
    Welcome to **SciProAI**—an enterprise-grade modular platform engineered to streamline molecular laboratory operations, 
    automate quality control and compliance, and drive advanced research.
    """)

    st.markdown("---")

    # Business Modules
    st.subheader("🏢 Business Modules")
    
    st.markdown("### QA/QC Auditor (`qcai`)")
    st.write("Audit instrument maintenance logs, batch release records, and environmental monitoring thresholds.")

    st.markdown("### Method & Assay Suite (`methodai`)")
    st.write("Format instrument data, calculate CLSI EP17 limits (LoB/LoD/LoQ), parse ddPCR droplets, and run method comparisons.")

    st.markdown("### SOP Compliance (`sopai`)")
    st.write("Manage standard operating procedures, track version histories, and verify document compliance.")

    st.markdown("---")

    # Research Modules
    st.subheader("🔬 Research Modules")
    
    st.markdown("### AssayAI Design (`assayai_design`)")
    st.write("Advanced molecular assay design and primer/probe evaluation suite.")

    st.markdown("### BiofilmAI Multimodal (`biofilmai_multimodal`)")
    st.write("Multimodal biofilm modeling and comparative analysis.")

    st.markdown("### BiofilmNN Diagnostics (`biofilmnn_diagnostics`)")
    st.write("Neural network diagnostics for microbial biofilms.")

    st.markdown("### Dashboards Visualization (`dashboards_visualization`)")
    st.write("Interactive data visualization dashboards for complex analytics.")

    st.markdown("### Biocontrol Inhibition (`biocontrol_inhibition`)")
    st.write("Antimicrobial inhibition and biocontrol analytics.")

    st.markdown("---")

    # Comprehensive Platform Guide & Directory
    st.subheader("📖 Platform Guide & Operational Directory")
    st.write("Detailed functional breakdown of all platform modules, system architecture, and underlying workflows.")

    st.markdown("#### Core Business Modules")
    st.info("""
    * **`qcai.py` (QA/QC Log & Audit Checker):** Audits instrument maintenance logs, environmental monitoring data, and batch release records against quality control thresholds.
    * **`methodai.py` (Method Performance, Verification & Assay Suite):** Formats raw instrument outputs, calculates quantitative linearity & amplification efficiency, computes CLSI EP17 detection limits (LoB, LoD, LoQ), processes digital PCR (ddPCR) Poisson partitioning, and executes method verification/comparison audits.
    * **`sopai.py` (SOP Version Control & Auditor):** Manages standard operating procedure documentation, tracks version changes, and audits procedural compliance.
    """)

    st.markdown("#### Research Modules")
    st.success("""
    * **`assayai_design.py`:** Advanced molecular assay design and primer/probe evaluation suite.
    * **`biofilmai_multimodal.py`:** Multimodal biofilm modeling and analysis.
    * **`biofilmnn_diagnostics.py`:** Neural network diagnostics for microbial biofilms.
    * **`dashboards_visualization.py`:** Interactive data visualization dashboards.
    * **`biocontrol_inhibition.py`:** Antimicrobial inhibition and biocontrol analytics.
    """)

    st.markdown("---")
    st.markdown("*Use the left sidebar navigation to switch directly between business and research modules.*")
