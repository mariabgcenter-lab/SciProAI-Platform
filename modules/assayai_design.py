import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # ---------------------------------------------------------
    # PAGE CONFIGURATION
    # ---------------------------------------------------------
    st.set_page_config(
        page_title="AssayAI — Molecular Assay Design Suite",
        layout="wide"
    )

    st.title("🧪 AssayAI — Molecular Assay Design Suite")
    st.write("""
    Design and explore **ddPCR/qPCR assays**, primer/probe sets,  
    and basic performance metrics for molecular diagnostics.
    """)

    # ---------------------------------------------------------
    # SIDEBAR NAVIGATION
    # ---------------------------------------------------------
    st.sidebar.header("AssayAI Modules")
    module = st.sidebar.radio(
        "Select a module:",
        [
            "Assay Design Workspace",
            "Primer/Probe Table Explorer",
            "Ct / Copy Number Calculator",
            "Assay Performance Preview"
        ]
    )

    # ---------------------------------------------------------
    # MODULE 1 — Assay Design Workspace
    # ---------------------------------------------------------
    if module == "Assay Design Workspace":
        st.subheader("🧬 Assay Design Workspace")

        target_name = st.text_input("Target name (gene, locus, pathogen):")
        forward_primer = st.text_input("Forward primer sequence (5'→3'):")
        reverse_primer = st.text_input("Reverse primer sequence (5'→3'):")
        probe_sequence = st.text_input("Probe sequence (optional):")

        if st.button("Generate Assay Summary"):
            if not target_name or not forward_primer or not reverse_primer:
                st.warning("Please enter target name and both primer sequences.")
            else:
                st.markdown("### Assay Summary")
                st.write(f"**Target:** {target_name}")
                st.write(f"**Forward Primer:** {forward_primer}")
                st.write(f"**Reverse Primer:** {reverse_primer}")
                if probe_sequence:
                    st.write(f"**Probe:** {probe_sequence}")
                st.write("""
                This assay design can be exported to validation plans,  
                SOPs, and ddPCR/qPCR optimization workflows.
                """)

    # ---------------------------------------------------------
    # MODULE 2 — Primer/Probe Table Explorer
    # ---------------------------------------------------------
    if module == "Primer/Probe Table Explorer":
        st.subheader("📋 Primer/Probe Table Explorer")

        uploaded = st.file_uploader("Upload primer/probe table (CSV)", type=["csv"])

        if uploaded:
            df = pd.read_csv(uploaded)
            st.write("### Table Preview")
            st.dataframe(df.head())

    # ---------------------------------------------------------
    # MODULE 3 — Ct / Copy Number Calculator
    # ---------------------------------------------------------
    if module == "Ct / Copy Number Calculator":
        st.subheader("📈 Ct / Copy Number Calculator")

        ct_value = st.number_input("Ct value", min_value=0.0, value=25.0)
        efficiency = st.number_input("PCR efficiency (0.0–1.0)", min_value=0.0, max_value=1.0, value=0.9)

        if st.button("Calculate Copy Number"):
            if efficiency <= 0:
                st.warning("Efficiency must be greater than 0.")
            else:
                # Simple illustrative formula
                copy_number = 10 ** ((40 - ct_value) * efficiency / 3.3)
                st.write("### Estimated Copy Number")
                st.success(f"{copy_number:.2e}")

    # ---------------------------------------------------------
    # MODULE 4 — Assay Performance Preview
    # ---------------------------------------------------------
    if module == "Assay Performance Preview":
        st.subheader("🧪 Assay Performance Preview")

        st.write("Enter basic performance metrics to visualize assay behavior.")

        lod = st.number_input("Limit of detection (copies/reaction)", min_value=0.0, value=10.0)
        loq = st.number_input("Limit of quantification (copies/reaction)", min_value=0.0, value=50.0)
        dynamic_low = st.number_input("Dynamic range lower bound (copies)", min_value=0.0, value=100.0)
        dynamic_high = st.number_input("Dynamic range upper bound (copies)", min_value=0.0, value=1e6)

        if st.button("Visualize Performance"):
            x = np.logspace(0, 6, 100)
            y = np.log10(x)

            fig, ax = plt.subplots(figsize=(8,5))
            ax.plot(x, y, label="Assay response (illustrative)")
            ax.axvline(lod, color="red", linestyle="--", label="LOD")
            ax.axvline(loq, color="orange", linestyle="--", label="LOQ")
            ax.axvspan(dynamic_low, dynamic_high, color="green", alpha=0.2, label="Dynamic range")
            ax.set_xscale("log")
            ax.set_xlabel("Copies per reaction")
            ax.set_ylabel("Signal (a.u.)")
            ax.set_title("Assay Performance Preview")
            ax.legend()
            st.pyplot(fig)
