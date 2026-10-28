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
    st.warning("⚠️ GEMINI_API_KEY not found in Streamlit Secrets. Please configure it in your app settings.")

# --- Sidebar Navigation ---
st.sidebar.title("SciProAI Navigation")
suite = st.sidebar.selectbox("Select Suite:", [
    "🏠 Home & Agent Assistant", 
    "🏢 Compliance & Quality Suite", 
    "🔬 Bio-Digital Research Suite"
])

st.sidebar.markdown("---")

active_module = None
domain = None

if suite == "🔬 Bio-Digital Research Suite":
    st.sidebar.subheader("Bio-Digital Domains")
    domain = st.sidebar.radio(
        "Select Domain:",
        ["AssayAI", "BiofilmAI", "BiofilmNN", "Dashboards", "Biocontrol"]
    )
    st.sidebar.markdown("---")
    
    if domain == "AssayAI":
        active_module = st.sidebar.selectbox("AssayAI Module:", [
            "Assay Design Workspace",
            "Primer/Probe Table Explorer",
            "Ct / Copy Number Calculator",
            "Assay Performance Preview"
        ])
    elif domain == "BiofilmAI":
        active_module = st.sidebar.selectbox("BiofilmAI Module:", [
            "Gene Expression Checker",
            "Biofilm Image Analyzer",
            "Multimodal Fusion Hub",
            "Research Document Summary"
        ])
    elif domain == "BiofilmNN":
        active_module = st.sidebar.selectbox("BiofilmNN Module:", [
            "Microbial Image Diagnostics",
            "AMR Prediction (AMRAI)",
            "Image Feature Extraction",
            "Diagnostic Reasoning Preview"
        ])
    elif domain == "Dashboards":
        active_module = st.sidebar.selectbox("Select Dashboard:", [
            "Gene Expression Dashboard",
            "Biofilm Behavior Dashboard",
            "MicrobiomeAI Dashboard",
            "Image Metrics Dashboard",
            "Fusion Data Dashboard"
        ])
    elif domain == "Biocontrol":
        active_module = st.sidebar.selectbox("Biocontrol Module:", [
            "Inhibition Dataset Explorer",
            "Compound Interaction Modeling",
            "Dose‑Response Visualization",
            "Inhibition Prediction Preview"
        ])

elif suite == "🏢 Compliance & Quality Suite":
    active_module = st.sidebar.selectbox("Compliance Module:", [
        "Compliance Workspace",
        "Audit Trail Explorer",
        "Quality Control Review"
    ])

elif suite == "🏠 Home & Agent Assistant":
    active_module = "Supervisor Overview"

# --- Main Content Area ---
st.title(f"SciProAI Platform // {suite}")

if domain:
    st.caption(f"Active Domain: **{domain}** | Active Module: **{active_module}**")
else:
    st.caption(f"Active Module: **{active_module}**")

st.markdown("---")

# --- Dynamic Module Workspace ---
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
    st.subheader(f"🏢 {active_module}")
    st.write("Professional compliance tracking, audit trails, and quality control metrics workspace.")
    # Add your compliance module specific UI elements here

elif suite == "🔬 Bio-Digital Research Suite":
    st.subheader(f"🔬 {domain} / {active_module}")
    st.write(f"Welcome to the **{active_module}** workspace. Configure parameters, analyze molecular data, or run predictions below.")
    
    # Example interactive container for your modules
    with st.container():
        st.markdown(f"### Interactive Workspace: {active_module}")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Enter Sample ID or Target Gene:")
            st.selectbox("Select Assay Model:", ["Standard RT-qPCR", "Digital PCR (ddPCR)", "Deep Learning Biofilm Model"])
        with col2:
            st.file_uploader("Upload Experimental Dataset (.csv, .xlsx, .fastq)")
        
        if st.button("Run Analysis"):
            st.spinner("Executing agentic pipeline...")
            st.success("Analysis complete! Results ready for review.")
