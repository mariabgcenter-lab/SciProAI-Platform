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
    
    st.markdown("### 📋 QA/QC Auditor (`qcai`)")
    st.write("Audit instrument maintenance logs, batch release records, and environmental monitoring thresholds.")

    st.markdown("### 📈 Method & Assay Suite (`methodai`)")
    st.write("Format instrument data, calculate CLSI EP17 limits (LoB/LoD/LoQ), parse ddPCR droplets, and run method comparisons.")

    st.markdown("### 📄 SOP Compliance (`sopai`)")
    st.write("Manage standard operating procedures, track version histories, and verify document compliance.")

    st.markdown("---")

    # Research Modules
    st.subheader("🔬 Research Modules")
    
    st.markdown("### `assayai_design`")
    st.write("Advanced molecular assay design and primer/probe evaluation suite.")

    st.markdown("### Biofilm & Biocontrol Suites")
    st.write("Multimodal modeling, neural network diagnostics, interactive visualization dashboards, and inhibition analytics.")

    st.markdown("---")
    st.markdown("*Use the left sidebar navigation to switch directly between business and research modules.*")
