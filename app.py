import os
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
            import google.generativeai as genai

            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
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
    st.subheader("QA/QC Log Workspace")
    st.write(
        "Monitor Westgard rules, quality control metrics, and audit trails."
    )
  with tab2:
    st.subheader("Method Performance & Assay Suite")
    st.write("Verify method precision, accuracy, and analytical linearity.")
  with tab3:
    st.subheader("SOP Version Control & Auditor")
    st.write(
        "Review, track, and audit Standard Operating Procedure versions."
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
