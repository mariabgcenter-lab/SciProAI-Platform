import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import streamlit as st
import modules.rag_engine as rag_engine


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
        extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        biofilmai_text = extracted if "Error" not in extracted else default_biofilmai_text
    else:
        biofilmai_text = default_biofilmai_text

    # ==========================================
    # 1. MULTIMODAL FEATURE INTEGRATOR
    # ==========================================
    if sub_tool == "🔬 1. Multimodal Feature Integrator (FISH + Omics)":
        st.subheader("🔬 Multimodal Data Integration (Spatial FISH + Transcriptomics + Clinical)")
        st.write("Synthesize spatial imaging signals, RNA-seq expression profiles, and clinical metadata into an integrated biofilm risk profile.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Spatial FISH & Microscopic Metrics")
            fish_intensity = st.slider("FISH Fluorescence Intensity (RFU)", 0, 1000, 680)
            cell_density = st.number_input("Microcolony Density (cells/µm²)", value=4.5, format="%.2f")
        with col2:
            st.markdown("##### Transcriptomic & EPS Expression")
            eps_gene_log2 = st.number_input("EPS Operon Fold Change (log2FC)", value=3.2, format="%.2f")
            efflux_log2 = st.number_input("Efflux Pump Expression (log2FC)", value=2.8, format="%.2f")

        if st.button("Compute Integrated Biofilm Risk Score", type="primary", use_container_width=True):
            norm_fish = min(1.0, fish_intensity / 1000.0)
            norm_density = min(1.0, cell_density / 10.0)
            norm_eps = min(1.0, max(0.0, eps_gene_log2 / 5.0))
            norm_efflux = min(1.0, max(0.0, efflux_log2 / 5.0))

            integrated_score = (norm_fish * 0.25) + (norm_density * 0.25) + (norm_eps * 0.30) + (norm_efflux * 0.20)

            i1, i2, i3, i4 = st.columns(4)
            i1.metric("FISH Signal Norm", f"{norm_fish:.2f}")
            i2.metric("EPS Upregulation", f"{eps_gene_log2:.1f} log2FC")
            i3.metric("Efflux Activity", f"{efflux_log2:.1f} log2FC")
            i4.metric(
                "Multimodal Risk Index", 
                f"{integrated_score:.3f}", 
                delta="High Tolerant Phenotype" if integrated_score > 0.60 else "Moderate Risk",
                delta_color="inverse" if integrated_score > 0.60 else "normal"
            )

    # ==========================================
    # 2. AMR GENOTYPE-TO-PHENOTYPE PREDICTOR
    # ==========================================
    elif sub_tool == "🧬 2. AMR Genotype-to-Phenotype Predictor":
        st.subheader("🧬 AMR Genotype-to-Phenotype Prediction Engine")
        st.write("Predict phenotypic antibiotic minimum inhibitory concentration (MIC) shifts based on detected resistance determinants and matrix protective barrier scores.")

        c1, c2 = st.columns(2)
        with c1:
            target_species = st.selectbox("Target Pathogen Species:", ["Pseudomonas aeruginosa", "Staphylococcus aureus", "Klebsiella pneumoniae", "Acinetobacter baumannii"])
            antibiotic_class = st.selectbox("Antibiotic Class:", ["Carbapenems (Meropenem)", "Fluoroquinolones (Ciprofloxacin)", "Aminoglycosides (Tobramycin)", "Glycopeptides (Vancomycin)"])
        with c2:
            amr_genes = st.multiselect("Detected AMR Genes & Mutations:", ["blaNDM-1", "mecA", "gyrA_S83L", "oprD_loss", "pelA_overexpression", "ndvB_active"], default=["blaNDM-1", "pelA_overexpression"])
            matrix_density = st.slider("Matrix EPS Barrier Score (0 = Planktonic, 1 = Dense Biofilm)", 0.0, 1.0, 0.75)

        if st.button("Predict AMR Phenotype & Fold MIC Shift", type="primary", use_container_width=True):
            base_fold = 1.0 + (len(amr_genes) * 4.5)
            matrix_fold_multiplier = 1.0 + (matrix_density * 15.0)
            predicted_total_shift = base_fold * matrix_fold_multiplier

            p1, p2, p3 = st.columns(3)
            p1.metric("Genotypic Resistance Markers", f"{len(amr_genes)} Genes Detected")
            p2.metric("Biofilm Matrix Shift", f"{matrix_fold_multiplier:.1f}x Barrier Protection")
            p3.metric("Predicted Total MIC Shift", f"{predicted_total_shift:.1f}x Fold Increase", delta="Severe Resistance")

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

        if st.button("Compute Effective Diffusion & Matrix Penetration", type="primary"):
            hydrodynamic_radius = 0.06 * (solute_mw ** 0.333)
            d_ratio = (np.exp(-np.pi * (polymer_vol_frac ** 0.5))) / tortuosity_factor
            if "Anionic" in matrix_charge and solute_mw < 1000:
                d_ratio *= 0.65  # Electrostatic binding retards cationic solute transport

            penetration_depth_um = 100.0 * np.sqrt(d_ratio)

            d1, d2, d3 = st.columns(3)
            d1.metric("Hydrodynamic Radius (nm)", f"{hydrodynamic_radius:.2f}")
            d2.metric("Effective Diffusion Ratio (Deff / D0)", f"{d_ratio:.4f}")
            d3.metric("Est. 30-Min Penetration Depth", f"{penetration_depth_um:.1f} µm")

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

        if st.button("Run Biofilm Protocol Audit Query", use_container_width=True):
            if query.strip():
                with st.spinner("Retrieving biofilm protocol context..."):
                    context = rag_engine.retrieve_relevant_context(query, biofilmai_text)
                    result = rag_engine.query_rag_engine(query, context, "Biofilm & AMR Multimodal Specialist")
                    st.success(result)
                    with st.expander("🔍 View Retrieved Context Snippets"):
                        st.code(context, language="text")
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

        if st.button("Run AI Multimodal Evaluation", type="primary"):
            if not multimodal_query.strip():
                st.warning("Please enter your query details.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                if not api_key:
                    st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables.")
                else:
                    with st.spinner("Analyzing multimodal biofilm data with Gemini AI..."):
                        try:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            context = rag_engine.retrieve_relevant_context(multimodal_query, biofilmai_text)

                            prompt = f"""
                            You are an expert biofilm computational biologist, AMR spatial transcriptomics specialist, and matrix biophysics researcher.
                            Provide comprehensive, professional analysis and recommendations for the following multimodal inquiry:

                            User Inquiry:
                            {multimodal_query}

                            Active Protocol / SOP Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            st.markdown("### 📋 AI Multimodal Expert Guidance")
                            st.success(response.text)
                        except Exception as e:
                            st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
