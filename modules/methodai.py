mport streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

def main():
    st.title("🏢 Method Performance, Verification & Assay Data Suite (`methodai`)")
    st.markdown("""
    Enterprise commercial module for parsing instrument exports, evaluating standard curve linearity, 
    computing CLSI EP17 detection limits, parsing digital PCR droplets, and running method comparison/verification audits.
    """)

    st.markdown("---")

    # Internal Sub-Navigation Menu (Prevents file uploader reset bugs caused by tabs)
    sub_tool = st.radio(
        "Select Method Module:",
        [
            "📈 1. Standard Curve & Efficiency", 
            "🎯 2. LoB, LoD & LoQ (CLSI EP17)", 
            "💧 3. ddPCR Droplet Analysis",
            "🔄 4. Intralab & Interlab Comparability",
            "⚖️ 5. Method Verification & Comparison Audit"
        ],
        horizontal=True
    )

    st.markdown("---")

    # ==========================================
    # 1. STANDARD CURVE & EFFICIENCY
    # ==========================================
    if sub_tool == "📈 1. Standard Curve & Efficiency":
        st.subheader("Quantitative Assay Linearity & Amplification Efficiency")
        st.write("Upload raw standard dilution exports (Log Concentration vs. Cq / RFU).")

        uploaded_file = st.file_uploader("Upload Standard Curve Data (CSV/Excel)", type=["csv", "xlsx", "xls"], key="sc_file")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            st.dataframe(df.head(3), use_container_width=True)
            
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(num_cols) >= 2:
                c1, c2 = st.columns(2)
                with c1: x_col = st.selectbox("Log Concentration / Copy Input:", num_cols, key="sc_x")
                with c2: y_col = st.selectbox("Measured Signal / Cq:", num_cols, key="sc_y", index=1)

                if st.button("Calculate Linearity & Efficiency", type="primary", key="sc_btn"):
                    clean_df = df[[x_col, y_col]].dropna()
                    slope, intercept, r_val, _, _ = stats.linregress(clean_df[x_col], clean_df[y_col])
                    r2 = r_val ** 2
                    try:
                        efficiency = (10 ** (-1 / slope) - 1) * 100
                    except:
                        efficiency = 0.0

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Linearity (R²)", f"{r2:.4f}", delta="Pass" if r2 >= 0.98 else "Review", delta_color="normal" if r2 >= 0.98 else "inverse")
                    m2.metric("Slope", f"{slope:.4f}")
                    m3.metric("Y-Intercept", f"{intercept:.4f}")
                    m4.metric("Efficiency (E%)", f"{efficiency:.1f}%", delta="Optimal (90-110%)" if 90 <= efficiency <= 110 else "Out of Range")
            else:
                st.error("Dataset requires at least two numeric columns.")

    # ==========================================
    # 2. LOB, LOD, & LOQ (CLSI EP17)
    # ==========================================
    elif sub_tool == "🎯 2. LoB, LoD & LoQ (CLSI EP17)":
        st.subheader("Limit of Blank (LoB), Detection (LoD), & Quantitation (LoQ)")
        st.write("Compute analytical cutoffs based on blank variance and low-level sample standard deviation.")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            blank_mean = st.number_input("Blank Mean", value=0.15, format="%.4f")
            blank_sd = st.number_input("Blank Standard Deviation", value=0.05, format="%.4f")
        with col_b2:
            low_sd = st.number_input("Low-Concentration Sample SD", value=0.12, format="%.4f")
            target_cv = st.number_input("Acceptable Precision Limit (%CV for LoQ)", value=20.0)

        if st.button("Compute LoB, LoD & LoQ", type="primary", key="lod_btn"):
            lob = blank_mean + (1.645 * blank_sd)
            lod = lob + (1.645 * low_sd)
            loq = lob + (3.3 * low_sd) 

            r1, r2, r3 = st.columns(3)
            r1.metric("Limit of Blank (LoB)", f"{lob:.4f}")
            r2.metric("Limit of Detection (LoD)", f"{lod:.4f}", delta="Primary Threshold")
            r3.metric("Limit of Quantitation (LoQ)", f"{loq:.4f}", delta=f"Target <{target_cv}% CV")

    # ==========================================
    # 3. DDPCR DROPLET ANALYSIS
    # ==========================================
    elif sub_tool == "💧 3. ddPCR Droplet Analysis":
        st.subheader("Digital PCR (ddPCR) Droplet Thresholding & Poisson Partitioning")
        
        uploaded_file = st.file_uploader("Upload Droplet Amplitude Export (CSV/Excel)", type=["csv", "xlsx", "xls"], key="dd_file")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                amp_col = st.selectbox("Select Droplet Amplitude Column (RFU):", num_cols, key="dd_amp")
                min_val, max_val = float(df[amp_col].min()), float(df[amp_col].max())
                threshold = st.slider("Fluorescence Amplitude Threshold", min_value=min_val, max_value=max_val, value=min_val + ((max_val - min_val) * 0.5))
                droplet_volume_nl = st.number_input("Assigned Droplet Volume (nL)", value=0.85)

                if st.button("Run Poisson Droplet Partitioning", type="primary", key="dd_btn"):
                    total_droplets = len(df)
                    positive_droplets = (df[amp_col] > threshold).sum()
                    negative_droplets = total_droplets - positive_droplets

                    if negative_droplets == 0:
                        st.error("Error: Zero negative droplets detected.")
                    else:
                        p_neg = negative_droplets / total_droplets
                        lambda_val = -np.log(p_neg)
                        concentration = lambda_val / (droplet_volume_nl * 1e-3)

                        d1, d2, d3, d4 = st.columns(4)
                        d1.metric("Total Droplets", f"{total_droplets:,}")
                        d2.metric("Positive Droplets", f"{positive_droplets:,}")
                        d3.metric("Negative Droplets", f"{negative_droplets:,}")
                        d4.metric("Concentration", f"{concentration:.2f} copies/uL", delta="Poisson Corrected")

    # ==========================================
    # 4. INTRALAB & INTERLAB COMPARABILITY
    # ==========================================
    elif sub_tool == "🔄 4. Intralab & Interlab Comparability":
        st.subheader("Intralab Precision & Interlab Method Comparability")
        
        analysis_mode = st.radio("Select Comparability Mode:", ["Intralab Run-to-Run Precision (EP05)", "Interlab / Multi-Site Bias Comparison (EP09)"], key="comp_mode")
        uploaded_file = st.file_uploader("Upload Comparability Dataset (CSV/Excel)", type=["csv", "xlsx", "xls"], key="comp_file")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

            if analysis_mode == "Intralab Run-to-Run Precision (EP05)" and len(num_cols) >= 1:
                c1, c2 = st.columns(2)
                with c1: val_col = st.selectbox("Select Measurement Value Column:", num_cols, key="intra_val")
                with c2: run_col = st.selectbox("Select Run / Day ID Column:", df.columns.tolist(), key="intra_run")

                if st.button("Calculate Intralab Precision (%CV)", type="primary", key="intra_btn"):
                    overall_mean = df[val_col].mean()
                    overall_std = df[val_col].std()
                    overall_cv = (overall_std / overall_mean) * 100
                    p1, p2, p3 = st.columns(3)
                    p1.metric("Grand Mean", f"{overall_mean:.3f}")
                    p2.metric("Intermediate SD", f"{overall_std:.3f}")
                    p3.metric("Total %CV", f"{overall_cv:.2f}%", delta="Target <15%" if overall_cv < 15 else "High CV")

            elif len(num_cols) >= 2:
                c1, c2 = st.columns(2)
                with c1: method_a = st.selectbox("Reference / Method A:", num_cols, key="inter_a")
                with c2: method_b = st.selectbox("Candidate / Method B:", num_cols, key="inter_b", index=1)

                if st.button("Evaluate Interlab Bias & Agreement", type="primary", key="inter_btn"):
                    clean_comp = df[[method_a, method_b]].dropna()
                    diff = clean_comp[method_b] - clean_comp[method_a]
                    mean_bias = diff.mean()
                    pct_bias = (mean_bias / clean_comp[method_a].mean()) * 100
                    b1, b2 = st.columns(2)
                    b1.metric("Mean Absolute Bias", f"{mean_bias:.4f}")
                    b2.metric("Mean Percentage Bias", f"{pct_bias:.2f}%")

    # ==========================================
    # 5. METHOD VERIFICATION & COMPARISON AUDIT
    # ==========================================
    elif sub_tool == "⚖️ 5. Method Verification & Comparison Audit":
        st.subheader("Method Verification vs. Validation Result Comparison")
        st.write("Compare candidate assay outputs against benchmark reference values or control runs.")

        protocol_type = st.radio("Select Compliance Objective:", ["Method Verification (Kit / Claim Confirmation)", "Full Method Validation / LDT Study"], key="audit_mode")
        uploaded_file = st.file_uploader("Upload Result Comparison Dataset (CSV/Excel)", type=["csv", "xlsx", "xls"], key="audit_file")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

            if len(num_cols) >= 2:
                c1, c2 = st.columns(2)
                with c1: test_col = st.selectbox("Candidate Results:", num_cols, key="audit_test")
                with c2: ref_col = st.selectbox("Reference Benchmark:", num_cols, key="audit_ref", index=1)

                tolerance_pct = st.slider("Acceptable Error Tolerance Limit (%)", min_value=1.0, max_value=25.0, value=10.0, step=0.5)

                if st.button("Execute Verification & Compliance Audit", type="primary", key="audit_btn"):
                    clean_audit = df[[test_col, ref_col]].dropna()
                    clean_audit["Absolute_Error"] = clean_audit[test_col] - clean_audit[ref_col]
                    clean_audit["Percent_Error"] = (abs(clean_audit["Absolute_Error"]) / clean_audit[ref_col]) * 100
                    clean_audit["Audit_Status"] = clean_audit["Percent_Error"].apply(lambda x: "PASS" if x <= tolerance_pct else "FAIL")

                    pass_count = (clean_audit["Audit_Status"] == "PASS").sum()
                    total_samples = len(clean_audit)
                    pass_rate = (pass_count / total_samples) * 100

                    v1, v2, v3 = st.columns(3)
                    v1.metric("Protocol Type", protocol_type.split("(")[0].strip())
                    v2.metric("Samples Meeting Tolerance", f"{pass_count} / {total_samples}")
                    v3.metric("Compliance Rate", f"{pass_rate:.1f}%", delta="Accepted" if pass_rate >= 90 else "Review Required", delta_color="normal" if pass_rate >= 90 else "inverse")

                    st.markdown("### Sample-by-Sample Comparison Table")
                    st.dataframe(clean_audit, use_container_width=True)
            else:
                st.error("Comparison audit requires at least two numeric columns.")
