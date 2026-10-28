import streamlit as st


def main():
  st.title("🧬 SciProAI Platform Hub & Guide")
  st.markdown("""
    Welcome to **SciProAI**—an enterprise-grade modular platform engineered to streamline molecular laboratory operations, 
    automate quality control and compliance, and drive advanced research powered by **Gemini 1.5-flash AI**.
    """)

  st.markdown("---")

  # Business Modules
  st.subheader("🏢 Business Modules")

  st.markdown("### QA/QC Auditor (`qcai`)")
  st.write(
      "Audit instrument maintenance logs, batch release records, and"
      " environmental monitoring thresholds."
  )

  st.markdown("### Method & Assay Suite (`methodai`)")
  st.write(
      "Format instrument data, calculate CLSI EP17 limits (LoB/LoD/LoQ), parse"
      " ddPCR droplets, and run method comparisons."
  )

  st.markdown("### SOP Compliance (`sopai`)")
  st.write(
      "Manage standard operating procedures, track version histories, and verify"
      " document compliance."
  )

  st.markdown("---")

  # Research Modules
  st.subheader("🔬 Research Modules")

  st.markdown("### AssayAI Design (`assayai_design`)")
  st.write(
      "Advanced molecular assay design and primer/probe evaluation suite with"
      " Gemini AI Advisor."
  )

  st.markdown("### BiofilmAI Multimodal (`biofilmai_multimodal`)")
  st.write(
      "Multimodal biofilm modeling, image analysis, and AI-powered literature"
      " summarization."
  )

  st.markdown("### BiofilmNN Diagnostics (`biofilmnn_diagnostics`)")
  st.write(
      "Neural network diagnostics, microbial image segmentation, and AI"
      " diagnostic reasoning."
  )

  st.markdown("### Dashboards Visualization (`dashboards_visualization`)")
  st.write(
      "Interactive data visualization dashboards and multi-omics fusion"
      " analytics."
  )

  st.markdown("### Biocontrol Inhibition (`biocontrol_inhibition`)")
  st.write(
      "Antimicrobial inhibition, compound interactions, and dose-response"
      " modeling."
  )

  st.markdown("---")

  # Platform AI Integration Highlights
  st.subheader("🤖 Platform AI & Agentic Capabilities")
  st.info("""
    * **Secure API Integration:** Powered by Google's **Gemini 1.5-flash**, securely initialized via `st.secrets` and `os.environ`.
    * **Specialized Expert Advisors:** Embedded directly into research and diagnostics modules for instant molecular biology, AMR, and assay troubleshooting.
    * **ReAct Agentic Workflow (`agent_assistant.py`):** Orchestrates automated function calling across business and research tools with bulletproof local fallback logic.
    """)

  st.markdown("---")

  # Comprehensive Platform Guide & Directory
  st.subheader("📖 Platform Guide & Operational Directory")
  st.write(
      "Detailed functional breakdown of all platform modules, system"
      " architecture, and underlying workflows."
  )

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
  st.markdown(
      "*Use the left sidebar navigation to switch directly between business and"
      " research modules.*"
  )
