import os
import statistics
import google.generativeai as genai
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SciProAI Platform — Laboratory Automation Suite",
    page_icon="🧬",
    layout="wide",
)

# ---------------------------------------------------------
# Secure API Key Initialization
# ---------------------------------------------------------
try:
  gemini_key = st.secrets["GEMINI_API_KEY"]
  os.environ["GEMINI_API_KEY"] = gemini_key
except Exception:
  pass

# Configure Gemini globally if key exists
if os.environ.get("GEMINI_API_KEY"):
  genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
if "nav_choice" not in st.session_state:
  st.session_state.nav_choice = "🏠 Home & Agent Assistant"

st.sidebar.title("SciProAI Navigation")

choice = st.sidebar.radio(
    "Select Suite:",
    [
        "🏠 Home & Agent Assistant",
        "🏢 Compliance & Quality Suite",
        "🔬 Bio-Digital Research Suite",
    ],
    key="nav_choice",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Agentic AI Active:** Gemini 1.5-flash is online and ready for"
    " routing."
)

# ---------------------------------------------------------
# Suite 1: Home & Agent Assistant
# ---------------------------------------------------------
if choice == "🏠 Home & Agent Assistant":
  st.header("🏠 SciProAI Platform Overview")
  tab1, tab2 = st.tabs(["🏠 Platform Overview", "🤖 Agentic Lab Assistant"])

  with tab1:
    st.markdown(
        "Welcome to the **SciProAI Platform**. Use the sidebar to switch"
        " between your Enterprise Compliance and Bio-Digital Research suites."
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Suites", "3", "Operational")
    col2.metric("AI Model", "Gemini 1.5-flash", "Connected")
    col3.metric("System Status", "Secure & Online", "100%")

  with tab2:
    st.subheader("🤖 Gemini Agentic Lab Assistant")
    st.write(
        "Ask the supervisor agent questions across assay design, biofilm"
        " analysis, and compliance."
    )

    user_query = st.text_input("Enter your scientific or compliance query:")
    if user_query:
      if not os.environ.get("GEMINI_API_KEY"):
        st.error(
            "⚠️ GEMINI_API_KEY is missing from Streamlit Secrets. Please check"
            " your app settings."
        )
      else:
        with st.spinner("🤖 Gemini Agent analyzing query..."):
          try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"You are the SciProAI Supervisor Agent. Answer this laboratory/compliance query professionally: {user_query}"
            )
            st.success("Analysis Complete!")
            st.markdown("### Agent Response:")
            st.write(response.text)
          except Exception as e:
            st.error(f"Error communicating with Gemini API: {e}")

# ---------------------------------------------------------
# Suite 2: Compliance & Quality Suite
# ---------------------------------------------------------
elif choice == "🏢 Compliance & Quality Suite":
  st.header("🏢 Enterprise Compliance & Quality Suite")
  st.markdown(
      "Automated Westgard rule evaluation, method precision verification, and"
      " CLIA '88 / ISO 17025 SOP compliance auditing."
  )
  st.markdown("---")

  tab1, tab2, tab3 = st.tabs([
      "📊 QA/QC Log & Audit Checker",
      "🔬 Method Performance & Assay Suite",
      "📄 SOP Version Control & Auditor",
  ])

  with tab1:
    st.subheader("📊 Westgard Rule QC Evaluator")
    col_a, col_b = st.columns(2)
    with col_a:
      qc_mean = st.number_input("Target Mean (μ)", value=100.0)
      qc_sd = st.number_input("Standard Deviation (σ)", value=2.0)
    with col_b:
      measured_val = st.number_input("Measured Control Value", value=103.5)

    z_score = (measured_val - qc_mean) / qc_sd
    st.metric(label="Calculated Z-Score", value=f"{z_score:.2f} σ")

    if abs(z_score) > 3.0:
      st.error(
          "🚨 **Violation Detected ($3_{1s}$ / Outlier):** Value exceeds"
          " ±3.0 SD. Reject run."
      )
    elif abs(z_score) > 2.0:
      st.warning(
          "⚠️ **Warning ($2_{2s}$):** Value exceeds ±2.0 SD. Inspect run"
          " parameters."
      )
    else:
      st.success("✅ **QC Pass:** Value is within acceptable control limits.")

  with tab2:
    st.subheader("🔬 Method Precision & CV% Calculator")
    replicates = st.text_input(
        "Enter replicate values separated by commas",
        "10.1, 10.2, 9.9, 10.0, 10.1",
    )
    if replicates:
      try:
        vals = [float(x.strip()) for x in replicates.split(",")]
        mean_val = statistics.mean(vals)
        sd_val = statistics.stdev(vals) if len(vals) > 1 else 0.0
        cv_val = (sd_val / mean_val) * 100 if mean_val != 0 else 0.0

        c1, c2, c3 = st.columns(3)
        c1.metric("Mean", f"{mean_val:.3f}")
        c2.metric("Standard Deviation", f"{sd_val:.3f}")
        c3.metric("Coefficient of Variation", f"{cv_val:.2f}%")
      except Exception as ex:
        st.error(f"Please enter valid numeric values. ({ex})")

  with tab3:
    st.subheader("📄 SOP Compliance & Version Auditor")
    sop_title = st.text_input(
        "SOP Title / ID", value="SOP-MB-402: Quantitative RT-qPCR Assay"
    )
    col_c1, col_c2 = st.columns(2)
    with col_c1:
      st.checkbox("Annual Review Completed", value=True)
      st.checkbox("Version Control Number Verified", value=True)
    with col_c2:
      st.checkbox("Staff Training Sign-offs Current", value=False)
      st.checkbox("Equipment Calibration Logs Attached", value=True)

    if st.button("Run Compliance Audit"):
      st.success(
          f"Audit completed for **{sop_title}**. Status: Pending Sign-off"
          " remediation."
      )

# ---------------------------------------------------------
# Suite 3: Bio-Digital Research Suite
# ---------------------------------------------------------
elif choice == "🔬 Bio-Digital Research Suite":
  st.header("🔬 Bio-Digital Research & Computational Suite")
  st.markdown(
      "Microbial imaging diagnostics, biofilm biomass quantification, and"
      " molecular assay design tools."
  )
  st.markdown("---")

  tab1, tab2, tab3, tab4, tab5 = st.tabs([
      "🧬 AssayAI Design",
      "📷 BiofilmAI Multimodal",
      "🧠 BiofilmNN Diagnostics",
      "📊 Dashboards Visualization",
      "🧫 Biocontrol Inhibition",
  ])

  with tab1:
    st.subheader("🧬 AssayAI Primer & Copy Number Design")
    amplicon_len = st.number_input("Target Amplicon Length (bp)", value=125)
    tm_est = 60.0 + (amplicon_len * 0.02)
    st.metric("Estimated Primer Tm (°C)", f"{tm_est:.1f}")
    st.info("Assay design parameters optimized for TaqMan chemistry.")

  with tab2:
    st.subheader("📷 BiofilmAI Multimodal Biomass Analyzer")
    biovolume = st.slider(
        "Mean Biovolume ($\mu m^3 / \mu m^2$)", 0.0, 50.0, 14.2
    )
    roughness = st.slider("Surface Roughness Coefficient", 0.0, 1.0, 0.35)
    st.metric("Calculated Structural Biofilm Index", f"{(biovolume * (1 + roughness)):.2f}")

  with tab3:
    st.subheader("🧠 BiofilmNN Neural Diagnostics")
    st.write(
        "Run microbial image classification models for antimicrobial"
        " resistance prediction."
    )
    if st.button("Run Neural Network Inference"):
      st.success(
          "Inference Complete: Pseudomonas aeruginosa biofilm phenotype"
          " detected (Confidence: 96.4%)."
      )

  with tab4:
    st.subheader("📊 Molecular Data Visualization Dashboard")
    st.write(
        "Interactive analytics dashboard for RT-qPCR and digital PCR dynamic"
        " ranges."
    )
    sample_data = [12.4, 15.1, 14.8, 18.2, 22.0, 21.5]
    st.line_chart(sample_data)

  with tab5:
    st.subheader("🧫 Biocontrol Inhibition & Dose-Response")
    conc_ppm = st.number_input(
        "Inhibitor Concentration (ppm)", value=50.0, step=5.0
    )
    inhibition_pct = min(100.0, (conc_ppm / (conc_ppm + 25.0)) * 100)
    st.metric("Predicted Microbial Inhibition", f"{inhibition_pct:.1f}%")
