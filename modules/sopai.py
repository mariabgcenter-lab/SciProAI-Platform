import streamlit as pd  # keeping imports clean
import streamlit as st

def main():
    # Note: Removed st.set_page_config here because app.py handles it globally!

    st.title("📘 SOPAI — SOP & Protocol Builder")
    st.write("""
    Design, structure, and **export laboratory SOPs, protocols, and workflows**  
    compliant with CLIA, ISO, CAP, and internal QA/QC standards.
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

        col1, col2 = st.columns(2)
        with col1:
            sop_title = st.text_input("SOP Title:", placeholder="e.g., DNA Extraction Protocol")
            sop_id = st.text_input("SOP ID / Code:", placeholder="e.g., SOP-MB-001")
            version = st.text_input("Version:", value="1.0")
        with col2:
            effective_date = st.text_input("Effective Date:", value="2026-03-30")
            author = st.text_input("Author / Owner:", value="BG BioWrite Scientific")

        sop_scope = st.text_area("Scope:")
        sop_purpose = st.text_area("Purpose:")
        sop_responsibilities = st.text_area("Responsibilities:")
        sop_materials = st.text_area("Materials / Reagents:")
        sop_procedure = st.text_area("Procedure (stepwise):")
        sop_qc = st.text_area("Quality Control / Acceptance Criteria:")
        sop_safety = st.text_area("Safety / Precautions:")

        if st.button("Generate & Format SOP", use_container_width=True):
            if not sop_title or not sop_id:
                st.warning("Please enter at least SOP Title and SOP ID.")
            else:
                # Compile into a professional Markdown document
                formatted_sop = f"""# Standard Operating Procedure
## {sop_title}

* **SOP ID:** {sop_id}
* **Version:** {version}
* **Effective Date:** {effective_date}
* **Author:** {author}

---

### 1. Purpose
{sop_purpose if sop_purpose else "N/A"}

### 2. Scope
{sop_scope if sop_scope else "N/A"}

### 3. Responsibilities
{sop_responsibilities if sop_responsibilities else "N/A"}

### 4. Materials & Reagents
{sop_materials if sop_materials else "N/A"}

### 5. Procedure
{sop_procedure if sop_procedure else "N/A"}

### 6. Quality Control & Acceptance Criteria
{sop_qc if sop_qc else "N/A"}

### 7. Safety & Precautions
{sop_safety if sop_safety else "N/A"}
"""

                st.success("✅ SOP Generated Successfully!")
                st.markdown("---")
                st.markdown(formatted_sop)

                # --- INSTANT DOWNLOAD BUTTON ---
                st.download_button(
                    label="📥 Download SOP Document (.md)",
                    data=formatted_sop,
                    file_name=f"{sop_id}_SOP.md",
                    mime="text/markdown",
                    use_container_width=True
                )

    # ---------------------------------------------------------
    # MODULE 2 — Stepwise Workflow Designer
    # ---------------------------------------------------------
    elif module == "Stepwise Workflow Designer":
        st.subheader("🔁 Stepwise Workflow Designer")
        st.write("Define stepwise procedures for laboratory workflows and export them.")

        steps = []
        num_steps = st.number_input("Number of steps", min_value=1, max_value=50, value=5)

        for i in range(int(num_steps)):
            step_desc = st.text_input(f"Step {i+1} description:", key=f"step_{i}")
            steps.append(step_desc)

        if st.button("Generate Workflow Document", use_container_width=True):
            workflow_text = "# Laboratory Workflow Protocol\n\n"
            for i, s in enumerate(steps, start=1):
                if s.strip():
                    workflow_text += f"### Step {i}\n{s}\n\n"

            st.markdown("### Preview")
            st.markdown(workflow_text)

            st.download_button(
                label="📥 Download Workflow (.md)",
                data=workflow_text,
                file_name="Workflow_Protocol.md",
                mime="text/markdown",
                use_container_width=True
            )

    # ---------------------------------------------------------
    # MODULE 3 — SOP Table Explorer
    # ---------------------------------------------------------
    elif module == "SOP Table Explorer":
        st.subheader("📋 SOP Table Explorer")
        uploaded = st.file_uploader("Upload SOP index or tracking table (CSV)", type=["csv"])

        if uploaded:
            df = pd.read_csv(uploaded)
            st.write("### SOP Table Preview")
            st.dataframe(df, use_container_width=True)
            st.info(f"Loaded {len(df)} records successfully.")
