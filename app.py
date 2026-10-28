import streamlit as st
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="SciProAI Platform",
    page_icon="🧬",
    layout="wide"
)

# --- Secure API Key Initialization ---
try:
    gemini_key = st.secrets["GEMINI_API_KEY"]
    os.environ["GEMINI_API_KEY"] = gemini_key
except Exception as e:
    st.warning("⚠️ GEMINI_API_KEY not found in Streamlit Secrets.")

# --- Clean Sidebar Navigation ---
st.sidebar.title("SciProAI Navigation")
suite = st.sidebar.selectbox("Select Suite:", [
    "🏠 Home & Agent Assistant", 
    "🏢 Compliance & Quality Suite", 
    "🔬 Bio-Digital Research Suite"
])

# --- Main Content Area ---
st.title(f"SciProAI Platform // {suite}")
st.markdown("---")

# --- Suite Workspaces ---
if suite == "🏠 Home & Agent Assistant":
    st.info("💡 **Agentic AI Active:** The Gemini Supervisor agent is online and ready to route queries across all modules.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Supervisor Agent Chat")
        user_prompt = st.text_input("Ask the SciProAI Assistant anything across your suites:")
        if user_prompt:
            st.success(f"Supervisor routing query: '{user_prompt}' to relevant modules...")
    with col2:
        st.metric(label="System Status", value="Secure & Online", delta="Gemini 1.5-flash")

elif suite == "🏢 Compliance & Quality Suite":
    st.subheader("🏢 Compliance & Quality Workspace")
    
    # Clean selectbox for Compliance modules
    compliance_module = st.selectbox("Select Compliance Module:", [
        "Compliance Workspace",
        "SOP & Regulatory Audit",
        "Quality Control Metrics",
        "CAPA & Risk Tracker"
    ])
    
    st.markdown(f"### Active Module: {compliance_module}")
    if compliance_module == "Compliance Workspace":
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Audits", "12", "Passed")
        col2.metric("SOP Compliance", "99.4%", "+0.2%")
        col3.metric("Pending QA Reviews", "2", "-1")
    else:
        st.write(f"Workspace for **{compliance_module}** loaded successfully.")

elif suite == "🔬 Bio-Digital Research Suite":
    st.subheader("🔬 Bio-Digital Research Domains")
    
    # Use clean tabs across the top instead of a messy sidebar radio button!
    tab_assay, tab_biofilm, tab_nn, tab_dash, tab_biocontrol = st.tabs([
        "🧬 AssayAI", 
        "🦠 BiofilmAI", 
        "🧠 BiofilmNN", 
        "📊 Dashboards", 
        "🧪 Biocontrol"
    ])
    
    with tab_assay:
        st.markdown("### AssayAI Modules")
        module = st.selectbox("Select AssayAI Module:", [
            "Assay Design Workspace",
            "Primer/Probe Table Explorer",
            "Ct / Copy Number Calculator",
            "Assay Performance Preview"
        ])
        st.info(f"Active Workspace: **{module}**")
        # Add your AssayAI UI code here
        
    with tab_biofilm:
        st.markdown("### BiofilmAI Modules")
        module = st.selectbox("Select BiofilmAI Module:", [
            "Gene Expression Checker",
            "Biofilm Image Analyzer",
            "Multimodal Fusion Hub",
            "Research Document Summary"
        ])
        st.info(f"Active Workspace: **{module}**")
        
    with tab_nn:
        st.markdown("### BiofilmNN Modules")
        module = st.selectbox("Select BiofilmNN Module:", [
            "Microbial Image Diagnostics",
            "AMR Prediction (AMRAI)",
            "Image Feature Extraction",
            "Diagnostic Reasoning Preview"
        ])
        st.info(f"Active Workspace: **{module}**")
        
    with tab_dash:
        st.markdown("### Research Dashboards")
        module = st.selectbox("Select Dashboard:", [
            "Gene Expression Dashboard",
            "Biofilm Behavior Dashboard",
            "MicrobiomeAI Dashboard",
            "Image Metrics Dashboard",
            "Fusion Data Dashboard"
        ])
        st.info(f"Active Workspace: **{module}**")
        
    with tab_biocontrol:
        st.markdown("### Biocontrol Modules")
        module = st.selectbox("Select Biocontrol Module:", [
            "Inhibition Dataset Explorer",
            "Compound Interaction Modeling",
            "Dose‑Response Visualization",
            "Inhibition Prediction Preview"
        ])
        st.info(f"Active Workspace: **{module}**")
