import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import streamlit as st

# Import platform shared RAG engine
try:
    from modules import rag_engine
except ImportError:
    import rag_engine


def main():
    st.title("🧫 BiofilmAI Multimodal AMR & Matrix Phenotyping Suite (`biofilmai_multimodal`)")
    st.markdown("""
    Advanced multimodal diagnostic suite combining fluorescence in situ hybridization (FISH), 
    transcriptomic gene expression, EPS matrix permeability modeling, and AMR genotype-to-phenotype neural prediction, backed by Gemini AI.
    """)

    st.markdown("---")

    # Sub-Navigation Menu
    sub_tool = st.radio(
        "Select Multimodal Module:",
        [
            "🔬 1. Multimodal Feature Integrator (FISH + Omics)",
            "🧬 2. AMR Genotype-to-Phenotype Predictor",
            "🧫 3. Matrix Permeability & EPS Dynamics",
            "⚖️ 4. Grounded Biofilm RAG Protocol Audit",
            "🤖 5. Gemini BiofilmAI Multimodal Advisor",
        ],
        horizontal=True,
    )

    st.markdown("---")

    # Sidebar PDF Protocol Intake for Grounded RAG
    st.sidebar.header("📁 Biofilm Protocol Intake")
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload Biofilm Protocol / Study (PDF)", 
        type=["pdf"], 
        help="Upload FISH staining protocols, transcriptomic AMR panels, or matrix permeability guidelines."
    )

    default_biofilmai_text = """
    BiofilmAI Multimodal & AMR Phenotyping Knowledge Base:
    1. FISH Signal Quantification: Hybridization probe fluorescence intensity SNR > 15.0 for species identification (e.g., P. aeruginosa, S. aureus).
    2. AMR Gene Markers: High-expression efflux pumps (MexAB-OprM, NorA) and matrix synthesis operons (pel/psl, pgaABCD) correlate with 100-fold MIC increases.
    3. EPS Permeability Dynamics: Effective solute diffusion coefficient Deff / D0 < 0.25 indicates severe steric hindrance by extracellular polysaccharides.
    4. Multimodal Risk Scoring: Combined FISH spatial density + log2FC gene expression + clinical MIC shift > 0.75 designates High Matrix Tolerance Phenotype.
    """

    if uploaded_pdf is not None:
        st.sidebar.success(f"📄 Custom Protocol: **{uploaded_pdf.name}**")
        if hasattr(rag_engine, "extract_text_from_pdf"):
            extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        else:
            extracted = "Error extracting PDF text."
        biofilmai_text = extracted if "Error" not in extracted else default_biofilmai_text
    else:
        biofilmai_text = default_biofilmai_text

    # ==========================================
    # 1. MULTIMODAL FEATURE INTEGRATOR (FISH + OMICS)
    # ==========================================
    if sub_tool == "🔬 1. Multimodal Feature Integrator (FISH + Omics)":
        st.subheader("🔬 Multimodal FISH & Transcriptomic Feature Integration")
        st.write("Combine FISH spatial hybridization fluorescence with log2FC gene expression for multimodal phenotypic risk scoring.")

        col1, col2 = st.columns(2)
        with col1:
            fish_snr = st.number_input("FISH Signal-to-Noise Ratio (SNR):", value=18.5, min_value=1.0, step=0.5)
            species_target = st.selectbox("Target Species (FISH Probe):", ["Pseudomonas aeruginosa", "Staphylococcus aureus", "Klebsiella pneumoniae", "Polymicrobial Mixture"])
        with col2:
            gene_log2fc = st.number_input("AMR / Operon Gene Expression (log2FC):", value=3.4, step=0.2)
            efflux_status = st.selectbox("Efflux Pump Expression Status:", ["Normal Baseline", "Moderate Upregulation", "Overexpressed (MexAB/NorA)"])

        if st.button("🔬 Integrate Multimodal Features", type="primary", use_container_width=True):
            snr_score = min(1.0, fish_snr / 25.0)
            fc_score = min(1.0, max(0.0, gene_log2fc / 5.0))
            composite_score = (snr_score * 0.4) + (fc_score * 0.6)
            is_high_risk = composite_score > 0.65

            st.markdown("### 📊 Multimodal Integration Metrics")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("FISH Probe SNR", f"{fish_snr:.1f}", "Specific Signal" if fish_snr >= 15.0 else "Weak Signal")
            with m2:
                st.metric("Gene Fold-Change", f"+{2**gene_log2fc:.1f}x", f"log2FC: {gene_log2fc:+.2f}")
            with m3:
                st.metric("Composite Risk Score", f"{composite_score:.2f}", "High Tolerance Risk" if is_high_risk else "Moderate", delta_color="inverse" if is_high_risk else "normal")

            integrator_report = (
                f"Multimodal Integration Summary:\n"
                f"- Target Species: {species_target}\n"
                f"- FISH Probe SNR: {fish_snr:.2f}\n"
                f"- Transcriptomic log2FC: {gene_log2fc:.2f} ({2**gene_log2fc:.1f}-fold change)\n"
                f"- Efflux Pump Status: {efflux_status}\n"
                f"- Composite Risk Score: {composite_score:.2f} / 1.00\n"
            )
            st.info(integrator_report)

            st.download_button(
                label="📥 Export Multimodal Integration Report (TXT)",
                data=integrator_report,
                file_name="multimodal_feature_integration_report.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ==========================================
    # 2. AMR GENOTYPE-TO-PHENOTYPE PREDICTOR
    # ==========================================
    elif sub_tool == "🧬 2. AMR Genotype-to-Phenotype Predictor":
        st.subheader("🧬 Neural Genotype-to-Phenotype MIC Shift Predictor")
        st.write("Predict phenotypic Minimal Inhibitory Concentration (MIC) shifts from underlying AMR resistance genotypes.")

        col1, col2 = st.columns(2)
        with col1:
            baseline_mic = st.number_input("Baseline MIC (µg/mL):", value=2.0, min_value=0.01, step=0.5)
            antimicrobial_class = st.selectbox("Antimicrobial Agent:", ["Tobramycin (Aminoglycoside)", "Ciprofloxacin (Fluoroquinolone)", "Meropenem (Carbapenem)", "Colistin (Polymyxin)"])
        with col2:
            operon_upregulation = st.checkbox("pel/psl Matrix Operon Upregulated", value=True)
            efflux_overexpression = st.checkbox("MexAB-OprM / NorA Overexpressed", value=True)

        if st.button("🧬 Predict Phenotypic MIC Shift", type="primary", use_container_width=True):
            fold_multiplier = 1.0
            if operon_upregulation:
                fold_multiplier *= 5.0
            if efflux_overexpression:
                fold_multiplier *= 10.0

            predicted_mic = baseline_mic * fold_multiplier
            is_resistant = predicted_mic > 16.0

            st.markdown("### 📊 Predicted AMR Phenotype Summary")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Baseline MIC", f"{baseline_mic:.2f} µg/mL")
            with m2:
                st.metric("Predicted Biofilm MIC", f"{predicted_mic:.1f} µg/mL", f"{fold_multiplier:.0f}-fold shift", delta_color="inverse" if fold_multiplier > 1.0 else "normal")
            with m3:
                st.metric("Phenotypic Classification", "RESISTANT" if is_resistant else "SUSCEPTIBLE", delta_color="inverse" if is_resistant else "normal")

            amr_report = (
                f"AMR Genotype-to-Phenotype Prediction Report:\n"
                f"- Agent: {antimicrobial_class}\n"
                f"- Baseline MIC: {baseline_mic:.2f} µg/mL\n"
                f"- Predicted Biofilm MIC: {predicted_mic:.2f} µg/mL ({fold_multiplier:.0f}x shift)\n"
                f"- Status: {'RESISTANT' if is_resistant else 'SUSCEPTIBLE'}\n"
            )
            st.info(amr_report)

            st.download_button(
                label="📥 Export AMR Prediction Report (TXT)",
                data=amr_report,
                file_name="amr_genotype_phenotype_report.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ==========================================
    # 3. MATRIX PERMEABILITY & EPS DYNAMICS
    # ==========================================
    elif sub_tool == "🧫 3. Matrix Permeability & EPS Dynamics":
        st.subheader("🧫 Extracellular Polymeric Substance (EPS) Permeability Modeling")
        st.write("Calculate effective solute diffusion coefficients ($D_{eff}/D_0$) through biofilm hydrogel matrices.")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            solute_mw = st.number_input("Antibiotic / Agent Molecular Weight (Da)", value=1420.5, help="e.g., Vancomycin ~1448 Da, Tobramycin ~467 Da")
            polymer_vol_frac = st.slider("EPS Hydrogel Polymer Volume Fraction (ϕ)", 0.01, 0.45, 0.18, step=0.01)
        with col_m2:
            matrix_charge = st.selectbox("EPS Matrix Charge Interaction:", ["Neutral / Uncharged", "Anionic Matrix (Alginate/DNA binding Cations)", "Cationic Matrix (Psl/Pel binding Anions)"])
            tortuosity_factor = st.number_input("Pore Structure Tortuosity Factor (τ)", value=1.85, format="%.2f")

        if st.button("Compute Effective Diffusion & Matrix Penetration", type="primary", use_container_width=True):
            hydrodynamic_radius = 0.06 * (solute_mw ** 0.333)
            d_ratio = (np.exp(-np.pi * (polymer_vol_frac ** 0.5))) / tortuosity_factor
            if "Anionic" in matrix_charge and solute_mw < 1000:
                d_ratio *= 0.65  # Electrostatic binding retards cationic solute transport

            penetration_depth_um = 100.0 * np.sqrt(d_ratio)

            # 1. 📊 Visual Metric Cards Row (st.metric)
            st.markdown("### 📊 EPS Hydrogel & Permeability Summary")
            d1, d2, d3 = st.columns(3)
            d1.metric("Hydrodynamic Radius (nm)", f"{hydrodynamic_radius:.2f}")
            d2.metric("Effective Diffusion Ratio (Deff / D0)", f"{d_ratio:.4f}", delta="Steric Hindrance" if d_ratio < 0.25 else "Normal", delta_color="inverse" if d_ratio < 0.25 else "normal")
            d3.metric("Est. 30-Min Penetration Depth", f"{penetration_depth_um:.1f} µm")

            eps_report = (
                f"EPS Matrix Permeability & Diffusion Summary:\n"
                f"- Solute Molecular Weight: {solute_mw:.1f} Da\n"
                f"- Hydrodynamic Radius: {hydrodynamic_radius:.2f} nm\n"
                f"- EPS Volume Fraction (ϕ): {polymer_vol_frac:.2f} | Tortuosity (τ): {tortuosity_factor:.2f}\n"
                f"- Charge Interaction: {matrix_charge}\n"
                f"- Effective Diffusion Ratio (Deff / D0): {d_ratio:.4f}\n"
                f"- Est. 30-Min Penetration Depth: {penetration_depth_um:.1f} µm\n"
            )
            st.info(eps_report)

            # 2. 📥 1-Click Export Button (st.download_button)
            st.download_button(
                label="📥 Export Matrix Permeability Calculation (TXT)",
                data=eps_report,
                file_name="eps_matrix_permeability_report.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ==========================================
    # 4. GROUNDED BIOFILM RAG PROTOCOL AUDIT
    # ==========================================
    elif sub_tool == "⚖️ 4. Grounded Biofilm RAG Protocol Audit":
        st.subheader("⚖️ Biofilm Multimodal & Phenotyping SOP RAG Audit")
        st.write("Cross-examine spatial imaging and AMR expression protocols against active uploaded manuals.")

        query = st.text_input(
            "Enter biofilm phenotyping or spatial transcriptomics query:",
            placeholder="e.g., What is the cutoff threshold for effective solute diffusion in dense P. aeruginosa alginate matrix?"
        )

        if st.button("Run Biofilm Protocol Audit Query", type="primary", use_container_width=True):
            if query.strip():
                # 1. 🤖 Animated Reasoning Status Container (st.status)
                with st.status("📜 Analyzing Biofilm Protocol & Retrieving Context...", expanded=True) as status:
                    try:
                        st.write("🔍 **Step 1: Inspecting biofilm knowledge base & retrieving context snippets...**")
                        if hasattr(rag_engine, "retrieve_relevant_context"):
                            context = rag_engine.retrieve_relevant_context(query, biofilmai_text)
                        else:
                            context = biofilmai_text

                        st.write("⚖️ **Step 2: Cross-examining protocols with Biofilm & AMR Specialist...**")
                        if hasattr(rag_engine, "query_rag_engine"):
                            result = rag_engine.query_rag_engine(query, context, "Biofilm & AMR Multimodal Specialist")
                        else:
                            result = f"Grounded Context Snippets:\n\n{context}"

                        status.update(
                            label="✅ Biofilm Protocol Audit Complete!",
                            state="complete",
                            expanded=False
                        )

                        # 2. 📊 Visual Metric Cards Row (st.metric)
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.metric("Protocol Source", "Uploaded PDF" if uploaded_pdf else "Embedded Default", delta=uploaded_pdf.name if uploaded_pdf else "BiofilmAI SOP")
                        with m2:
                            st.metric("RAG Grounding", "Active", delta="Context Grounded")
                        with m3:
                            st.metric("Audit Readiness", "Complete", delta="Report Ready")

                        # Output Display
                        st.markdown("#### 📑 Compliance Audit Findings")
                        st.success(result)

                        with st.expander("🔍 View Retrieved Context Snippets"):
                            st.code(context, language="text")

                        # 3. 📥 1-Click Export Button (st.download_button)
                        st.download_button(
                            label="📥 Export Biofilm Protocol Audit Findings (TXT)",
                            data=f"Query: {query}\n\nAudit Findings:\n{result}\n\nRetrieved Context:\n{context}",
                            file_name="biofilm_protocol_audit_findings.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                    except Exception as e:
                        status.update(label="❌ Audit Analysis Execution Error", state="error")
                        st.error(f"Execution Error: {e}")
            else:
                st.warning("Please enter a query above.")

    # ==========================================
    # 5. GEMINI BIOFILMAI MULTIMODAL ADVISOR
    # ==========================================
    elif sub_tool == "🤖 5. Gemini BiofilmAI Multimodal Advisor":
        st.subheader("🤖 Gemini BiofilmAI Multimodal & AMR AI Advisor")
        st.write("Consult the AI advisor for assistance with spatial transcriptomics, EPS matrix transport modeling, and AMR phenotype prediction.")

        multimodal_query = st.text_area(
            "Describe your multimodal dataset, FISH hybridization finding, or matrix penetration query:",
            placeholder="e.g., We observe high pelA gene upregulation but low tobramycin clearance in S. aureus / P. aeruginosa co-culture."
        )

        if st.button("Run AI Multimodal Evaluation", type="primary", use_container_width=True):
            if not multimodal_query.strip():
                st.warning("Please enter your query details.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                if not api_key:
                    st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables.")
                else:
                    # 1. 🤖 Animated Reasoning Status Container (st.status)
                    with st.status("Analyzing multimodal biofilm data with Gemini AI...", expanded=True) as status:
                        try:
                            st.write("🔍 **Step 1: Retrieving active biofilm protocol & RAG context...**")
                            if hasattr(rag_engine, "retrieve_relevant_context"):
                                context = rag_engine.retrieve_relevant_context(multimodal_query, biofilmai_text)
                            else:
                                context = biofilmai_text

                            st.write("🧬 **Step 2: Synthesizing spatial transcriptomics & matrix biophysics model...**")
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")

                            prompt = f"""
                            You are an expert biofilm computational biologist, AMR spatial transcriptomics specialist, and matrix biophysics researcher.
                            Provide comprehensive, professional analysis and recommendations for the following multimodal inquiry:

                            User Inquiry:
                            {multimodal_query}

                            Active Protocol / SOP Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            report_text = response.text

                            status.update(
                                label="✅ Multimodal Biofilm Evaluation Complete!",
                                state="complete",
                                expanded=False
                            )

                            # 2. 📊 Visual Metric Cards Row (st.metric)
                            m1, m2, m3 = st.columns(3)
                            with m1:
                                st.metric("Multimodal Model", "Spatial Omics", delta="FISH + Permeability")
                            with m2:
                                st.metric("AMR Advisor Engine", "Active", delta="Gemini 1.5 Flash")
                            with m3:
                                st.metric("Export Readiness", "Complete", delta="Report Export Ready")

                            st.markdown("### 📋 AI Multimodal Expert Guidance")
                            st.success(report_text)

                            # 3. 📥 1-Click Export Button (st.download_button)
                            st.download_button(
                                label="📥 Export Multimodal AI Report (TXT)",
                                data=report_text,
                                file_name="sciproai_multimodal_advisor_report.txt",
                                mime="text/plain",
                                help="Click to save a local copy of this multimodal evaluation.",
                                use_container_width=True
                            )

                        except Exception as e:
                            status.update(label="❌ Analysis Execution Error", state="error")
                            st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
