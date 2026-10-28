import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import streamlit as st


def main():
  st.title("🏢 QA/QC Log & Audit Checker (`qcai`)")
  st.markdown("""
    Upload daily instrument logs, assay control runs, or quality control metrics to instantly 
    flag statistical outliers, missing data fields, and non-conformance trends before internal or external audits, backed by Gemini AI.
    """)

  st.markdown("---")

  # Internal Sub-Navigation Menu (Tabs/Radio to include AI Advisor)
  sub_tool = st.radio(
      "Select QA/QC Module:",
      ["📊 QC Log Audit Engine", "🤖 Gemini QA/QC AI Advisor"],
      horizontal=True,
  )

  st.markdown("---")

  if sub_tool == "📊 QC Log Audit Engine":
    # Layout: Two columns for configuration and upload
    col1, col2 = st.columns([2, 1])

    with col1:
      uploaded_file = st.file_uploader(
          "Upload Daily QC Log / Instrument Data (CSV or Excel)",
          type=["csv", "xlsx", "xls"],
      )

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

    # Provide a sample data option for instant testing
    if uploaded_file is None:
      st.info(
          "Upload your QC log file above, or load the sample dataset below to"
          " test the audit engine right now."
      )
      if st.button("Load Sample QC Log Dataset", use_container_width=True):
        # Create a realistic sample DataFrame with an injected outlier
        np.random.seed(42)
        dates = pd.date_range(start="2026-08-01", periods=30, freq="D")
        sample_data = {
            "Date": dates,
            "Instrument_ID": np.random.choice(
                ["Inst-A", "Inst-B", "Inst-C"], size=30
            ),
            "Assay_ID": "qPCR-Pathogen-V1",
            "Control_Value": np.random.normal(100.0, 4.0, size=30),
            "Operator": np.random.choice(
                ["J. Smith", "A. Davis", "M. Gomez"], size=30
            ),
            "Status": "Pass",
        }
        # Inject a couple of intentional outliers/missing values to demonstrate auditing
        sample_data["Control_Value"][6] = 115.8  # Outlier high
        sample_data["Control_Value"][21] = 84.1  # Outlier low

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

    if df is not None:
      st.markdown("---")
      st.subheader("📊 Data Preview")
      st.dataframe(df.head(10), use_container_width=True)

      st.markdown("---")
      st.subheader("🔍 Automated QC & Outlier Audit")

      if st.button("Execute QC Audit", type="primary", use_container_width=True):
        with st.spinner(
            "Analyzing data distribution and checking audit criteria..."
        ):

          # Identify numeric control value columns
          numeric_cols = df.select_dtypes(
              include=[np.number]
          ).columns.tolist()

          if not numeric_cols:
            st.error(
                "No numeric columns found for statistical outlier analysis."
                " Ensure your log contains numerical measurement or control"
                " values."
            )
            return

          # Select the primary numeric column for audit
          target_col = numeric_cols[0]

          # Calculate mean and standard deviation
          mean_val = df[target_col].mean()
          std_val = df[target_col].std()

          # Flag outliers based on SD threshold
          lower_limit = mean_val - (sd_threshold * std_val)
          upper_limit = mean_val + (sd_threshold * std_val)

          df["Outlier_Flag"] = df[target_col].apply(
              lambda x: (
                  "OUTLIER" if (x < lower_limit or x > upper_limit) else "Normal"
              )
          )

          # Check missing values
          missing_mask = (
              df.isnull().any(axis=1)
              if check_missing
              else pd.Series([False] * len(df))
          )

          outlier_count = (df["Outlier_Flag"] == "OUTLIER").sum()
          missing_count = missing_mask.sum()

          # Metrics display
          m1, m2, m3, m4 = st.columns(4)
          m1.metric("Total Records Audited", len(df))
          m2.metric("Mean Control Value", f"{mean_val:.2f}")
          m3.metric(
              "Statistical Outliers",
              outlier_count,
              delta=(
                  "Review Required" if outlier_count > 0 else "None"
              ),
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

            # Filter to show flagged rows only
            flagged_df = df[(df["Outlier_Flag"] == "OUTLIER") | missing_mask]
            st.dataframe(flagged_df, use_container_width=True)
          else:
            st.success(
                "Clean Audit! No statistical outliers or missing mandatory"
                " fields detected within the specified threshold."
            )

          # Full dataset with status flags
          with st.expander("View Full Audited Dataset (With Outlier Tags)"):
            st.dataframe(df, use_container_width=True)

  elif sub_tool == "🤖 Gemini QA/QC AI Advisor":
    st.subheader("🤖 Gemini QA/QC & CAPA Compliance Advisor")
    st.write(
        "Consult the AI advisor for expert root-cause analysis, corrective and"
        " preventive action (CAPA) drafting, and audit preparation guidance."
    )

    qa_query = st.text_area(
        "Describe your non-conformance event, out-of-specification (OOS)"
        " finding, or instrument QC trend:"
    )

    if st.button("Run AI QA Evaluation", type="primary"):
      if not qa_query.strip():
        st.warning("Please enter your QC event details.")
      else:
        api_key = st.secrets.get(
            "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")
        )
        if not api_key:
          st.error(
              "⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment"
              " Variables."
          )
        else:
          with st.spinner("Analyzing quality control event..."):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert quality assurance manager, laboratory compliance auditor, and ISO/CLIA specialist. 
                            Provide rigorous, professional root-cause analysis and actionable CAPA (Corrective and Preventive Action) recommendations for the following QA/QC event:
                            {qa_query}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 AI QA Expert Guidance & CAPA Plan")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")
