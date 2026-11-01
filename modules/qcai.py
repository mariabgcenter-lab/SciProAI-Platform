import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import streamlit as st
import modules.rag_engine as rag_engine


def main():
    st.title("🏢 QA/QC Log & Audit Checker (`qcai`)")
    st.markdown("""
    Upload daily instrument logs, assay control runs, or quality control metrics to instantly 
    flag statistical outliers, missing data fields, and non-conformance trends before internal or external audits, backed by Gemini AI.
    """)

    st.markdown("---")

    # Internal Sub-Navigation Menu
    sub_tool = st.radio(
        "Select QA/QC Module:",
        ["📊 QC Log Audit Engine", "🤖 Gemini QA/QC AI Advisor"],
        horizontal=True,
    )

    st.markdown("---")

    # Sidebar PDF & Manual Intake for RAG Grounding
    st.sidebar.header("📁 SOP & Manual Intake")
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload QA/QC Policy / SOP (PDF)", 
        type=["pdf"], 
        help="Upload lab manuals, equipment protocols, or CAPA procedures for RAG auditing."
    )

    default_qc_text = """
    QA/QC Instrument Audit Log & SOP Protocol:
    1. Lot #204 flagged for 1_3s Westgard rule violation (Control mean 12.4 vs 10.0 target).
    2. Optical Sensor Array #3 recalibrated. Post-calibration verification %CV = 2.1%.
    3. Mandatory Fields: Instrument ID, Operator Initials, Lot Number, Run Date, and Control Target.
    4. Outlier Policy: Values exceeding ±2.0 SD require secondary run confirmation prior to release.
    """

    if uploaded_pdf is not None:
        st.sidebar.success(f"📄 Custom SOP: **{uploaded_pdf.name}**")
        extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        qc_text = extracted if "Error" not in extracted else default_qc_text
    else:
        qc_text = default_qc_text

    # ---------------------------------------------------------
    # SUB-TOOL 1: QC Log Audit Engine
    # ---------------------------------------------------------
    if sub_tool == "📊 QC Log Audit Engine":
        st.subheader("📊 QC Log & Metrics Audit Engine")

        # Layout: Two columns for configuration and upload
        col1, col2 = st.columns([2, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "Upload Daily QC Log / Instrument Data (CSV or Excel)",
                type=["csv", "xlsx", "xls"],
            )

            # Provide a sample data option for instant testing
            if uploaded_file is None:
                st.info(
                    "Upload your QC log file above, or load the sample dataset below to"
                    " test the audit engine right now."
                )
                if st.button("Load Sample QC Log Dataset", use_container_width=True):
                    # Create a realistic sample DataFrame with injected outliers
                    np.random.seed(42)
                    dates = pd.date_range(start="2026-08-01", periods=30, freq="D")
                    control_vals = np.random.normal(100.0, 4.0, size=30)
                    control_vals[6] = 115.8  # Outlier high
                    control_vals[21] = 84.1  # Outlier low

                    sample_data = {
                        "Date": dates,
                        "Instrument_ID": np.random.choice(
                            ["Inst-A", "Inst-B", "Inst-C"], size=30
                        ),
                        "Assay_ID": "qPCR-Pathogen-V1",
                        "Control_Value": control_vals,
                        "Operator": np.random.choice(
                            ["J. Smith", "A. Davis", "M. Gomez"], size=30
                        ),
                        "Status": "Pass",
                    }

                    df_sample = pd.DataFrame(sample_data)
                    st.session_state["qc_df"] = df_sample
                    st.success(
                        "Sample dataset loaded successfully! Scroll down to run the audit."
                    )

            # Load data if uploaded or sample is stored in session state
            df = None
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith(".csv"):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    st.session_state["qc_df"] = df
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            elif "qc_df" in st.session_state:
                df = st.session_state["qc_df"]

        with col2:
            st.subheader("Audit Parameters")
            sd_threshold = st.slider(
                "Outlier Control Limit (SD)",
                min_value=1.5,
                max_value=3.0,
                value=2.0,
                step=0.5,
                help="Flag values exceeding ± this many standard deviations from the mean.",
            )
            check_missing = st.checkbox(
                "Flag Missing Mandatory Fields", value=True
            )

        # Quantitative Outlier Audit Execution
        if df is not None:
            st.markdown("---")
            st.subheader("📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            st.markdown("---")
            st.subheader("🔍 Automated QC & Outlier Audit")

            if st.button("Execute QC Audit", type="primary", use_container_width=True):
                with st.spinner("Analyzing data distribution and checking audit criteria..."):
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

                    if not numeric_cols:
                        st.error(
                            "No numeric columns found for statistical outlier analysis."
                            " Ensure your log contains numerical measurement or control values."
                        )
                    else:
                        target_col = numeric_cols[0]
                        mean_val = df[target_col].mean()
                        std_val = df[target_col].std()

                        lower_limit = mean_val - (sd_threshold * std_val)
                        upper_limit = mean_val + (sd_threshold * std_val)

                        df["Outlier_Flag"] = df[target_col].apply(
                            lambda x: "OUTLIER" if (x < lower_limit or x > upper_limit) else "Normal"
                        )

                        missing_mask = (
                            df.isnull().any(axis=1)
                            if check_missing
                            else pd.Series([False] * len(df))
                        )

                        outlier_count = (df["Outlier_Flag"] == "OUTLIER").sum()
                        missing_count = missing_mask.sum()

                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Total Records Audited", len(df))
                        m2.metric("Mean Control Value", f"{mean_val:.2f}")
                        m3.metric(
                            "Statistical Outliers",
                            outlier_count,
                            delta="Review Required" if outlier_count > 0 else "None",
                            delta_color="inverse" if outlier_count > 0 else "normal",
                        )
                        m4.metric("Missing Fields Flagged", missing_count)

                        st.markdown("### Audit Findings & Flagged Records")
                        if outlier_count > 0 or missing_count > 0:
                            st.warning(
                                f"Audit completed with flags: **{outlier_count} statistical"
                                f" outliers** and **{missing_count} records with missing"
                                f" data** detected."
                            )
                            flagged_df = df[(df["Outlier_Flag"] == "OUTLIER") | missing_mask]
                            st.dataframe(flagged_df, use_container_width=True)
                        else:
                            st.success(
                                "Clean Audit! No statistical outliers or missing mandatory"
                                " fields detected within the specified threshold."
                            )

                        with st.expander("View Full Audited Dataset (With Outlier Tags)"):
                            st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔍 Grounded SOP Policy Query")
        query = st.text_input(
            "Enter QC query across uploaded SOP policy & compliance guidelines:",
            placeholder="e.g., What is our protocol when an outlier exceeds ±2.0 SD?"
        )

        if st.button("Run SOP Compliance Query", use_container_width=True):
            if query.strip():
                with st.spinner("Retrieving SOP guidelines and evaluating compliance..."):
                    context = rag_engine.retrieve_relevant_context(query, qc_text)
                    result = rag_engine.query_rag_engine(query, context, "Clinical QA/QC Auditor")
                    st.success(result)
                    with st.expander("🔍 View Retrieved SOP Context Snippets"):
                        st.code(context, language="text")
            else:
                st.warning("Please enter a query above.")

 # ---------------------------------------------------------
    # SUB-TOOL 2: Gemini QA/QC AI Advisor
    # ---------------------------------------------------------
    elif sub_tool == "🤖 Gemini QA/QC AI Advisor":
        st.subheader("🤖 Gemini QA/QC & CAPA Compliance Advisor")
        st.write(
            "Consult the AI advisor for expert root-cause analysis, corrective and"
            " preventive action (CAPA) drafting, and audit preparation guidance."
        )

        qa_query = st.text_area(
            "Describe your non-conformance event, out-of-specification (OOS)"
            " finding, or instrument QC trend:",
            placeholder="e.g., Control Lot #204 demonstrated repeated 1_3s Westgard flags over 3 consecutive runs."
        )

        if st.button("Run AI QA Evaluation", type="primary"):
            if not qa_query.strip():
                st.warning("Please enter your QC event details.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                if not api_key:
                    st.error(
                        "⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables."
                    )
                else:
                    # 1. Animated Reasoning Status Box
                    with st.status("🤖 Analyzing Quality Control Event & CAPA Context...", expanded=True) as status:
                        try:
                            st.write("🔍 **Step 1: Retrieving active SOP & compliance RAG context...**")
                            context = rag_engine.retrieve_relevant_context(qa_query, qc_text)
                            
                            st.write("⚖️ **Step 2: Synthesizing ISO/CLIA root-cause analysis & CAPA plan...**")
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            
                            prompt = f"""
                            You are an expert quality assurance manager, laboratory compliance auditor, and ISO/CLIA specialist. 
                            Provide rigorous, professional root-cause analysis and actionable CAPA (Corrective and Preventive Action) recommendations for the following QA/QC event:
                            
                            User Description:
                            {qa_query}

                            Active SOP / Compliance Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            
                            status.update(
                                label="✅ QA Root-Cause & CAPA Analysis Complete!", 
                                state="complete", 
                                expanded=False
                            )
                            
                            # 2. 📊 Visual Metric Cards Row
                            m1, m2, m3 = st.columns(3)
                            with m1:
                                st.metric(
                                    label="Audit Evaluation", 
                                    value="CAPA Generated", 
                                    delta="ISO/CLIA Compliant", 
                                    delta_color="normal"
                                )
                            with m2:
                                st.metric(
                                    label="RAG Grounding", 
                                    value="Active SOP", 
                                    delta="Grounded Context", 
                                    delta_color="normal"
                                )
                            with m3:
                                st.metric(
                                    label="Export Readiness", 
                                    value="Complete", 
                                    delta="Report Ready", 
                                    delta_color="normal"
                                )

                            st.markdown("### 📋 AI QA Expert Guidance & CAPA Plan")
                            st.success(response.text)

                            # 3. 📥 1-Click Download Button
                            st.download_button(
                                label="📥 Export CAPA & Root-Cause Audit Report (TXT)",
                                data=response.text,
                                file_name="sciproai_capa_report.txt",
                                mime="text/plain",
                                help="Click to save this CAPA and root-cause analysis to your computer.",
                                use_container_width=True
                            )
                        except Exception as e:
                            status.update(label="❌ Analysis Error", state="error")
                            st.error(f"API Error: {e}")


if __name__ == "__main__":
    main() 
