import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SOPAI — SOP & Protocol Builder",
    layout="wide"
)

st.title("📘 SOPAI — SOP & Protocol Builder")
st.write("""
Design and structure **laboratory SOPs, protocols, and workflows**  
for CLIA, ISO, CAP, and internal QA/QC operations.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("SOPAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "SOP Template Builder",
        "Stepwise Workflow Designer",
        "SOP Table Explorer"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — SOP Template Builder
# ---------------------------------------------------------
if module == "SOP Template Builder":
    st.subheader("🧾 SOP Template Builder")

    sop_title = st.text_input("SOP Title:")
    sop_id = st.text_input("SOP ID / Code:")
    sop_scope = st.text_area("Scope:")
    sop_purpose = st.text_area("Purpose:")
    sop_responsibilities = st.text_area("Responsibilities:")
    sop_materials = st.text_area("Materials / Reagents:")
    sop_procedure = st.text_area("Procedure (stepwise):")
    sop_qc = st.text_area("Quality Control / Acceptance Criteria:")
    sop_safety = st.text_area("Safety / Precautions:")

    if st.button("Generate SOP Summary"):
        if not sop_title or not sop_id:
            st.warning("Please enter at least SOP Title and SOP ID.")
        else:
            st.markdown("### SOP Summary")
            st.write(f"**Title:** {sop_title}")
            st.write(f"**ID:** {sop_id}")
            st.write(f"**Scope:** {sop_scope}")
            st.write(f"**Purpose:** {sop_purpose}")
            st.write(f"**Responsibilities:** {sop_responsibilities}")
            st.write(f"**Materials / Reagents:** {sop_materials}")
            st.write(f"**Procedure:**\n{sop_procedure}")
            st.write(f"**Quality Control / Acceptance Criteria:** {sop_qc}")
            st.write(f"**Safety / Precautions:** {sop_safety}")

# ---------------------------------------------------------
# MODULE 2 — Stepwise Workflow Designer
# ---------------------------------------------------------
if module == "Stepwise Workflow Designer":
    st.subheader("🔁 Stepwise Workflow Designer")

    st.write("Define stepwise procedures for laboratory workflows.")

    steps = []
    num_steps = st.number_input("Number of steps", min_value=1, max_value=50, value=5)

    for i in range(int(num_steps)):
        step_desc = st.text_input(f"Step {i+1} description:", key=f"step_{i}")
        steps.append(step_desc)

    if st.button("Generate Workflow"):
        st.markdown("### Workflow Steps")
        for i, s in enumerate(steps, start=1):
            if s.strip():
                st.write(f"**Step {i}:** {s}")

# ---------------------------------------------------------
# MODULE 3 — SOP Table Explorer
# ---------------------------------------------------------
if module == "SOP Table Explorer":
    st.subheader("📋 SOP Table Explorer")

    uploaded = st.file_uploader("Upload SOP index or tracking table (CSV)", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### SOP Table Preview")
        st.dataframe(df.head())
