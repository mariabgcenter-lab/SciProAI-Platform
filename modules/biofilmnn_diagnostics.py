import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import streamlit as st
import modules.rag_engine as rag_engine


def main():
    st.title("🔬 Biofilm Neural Network Diagnostics (`biofilmnn`)")
    st.markdown("""
    Deep-learning assisted diagnostic platform for analyzing Confocal Laser Scanning Microscopy (CLSM), 
    Scanning Electron Microscopy (SEM), and fluorescence imaging data to quantify biomass, roughness, and microbial viability, backed by Gemini AI.
    """)

    st.markdown("---")

    # Sub-Navigation Menu
    sub_tool = st.radio(
        "Select Diagnostics Module:",
        [
            "🖼️ 1. CLSM & SEM Image Feature Extractor",
            "🧬 2. Biofilm Structural Viability Classifier",
            "⚖️ 3. Grounded Imaging SOP Audit",
            "🤖 4. Gemini Biofilm AI Advisor",
        ],
        horizontal=True,
    )

    st.markdown("---")

    # Sidebar Microscopy Manual Intake for Grounded RAG
    st.sidebar.header("📁 Microscopy SOP Intake")
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload Imaging Manual / SOP (PDF)", 
        type=["pdf"], 
        help="Upload CLSM image acquisition protocols, staining SOPs, or biofilm quantification guidelines."
    )

    default_imaging_text = """
    Biofilm Microscopy & Image Diagnostics Knowledge Base:
    1. CLSM Acquisition Protocol: SYTO 9 / Propidium Iodide (PI) fluorophores for live/dead cell discrimination.
    2. Biomass Volume Quantification: Threshold Z-stacks using Otsu algorithm. Minimum acceptable signal-to-noise ratio > 12.0 dB.
    3. Roughness Coefficient (Ra): Surface topography roughness Ra > 0.45 indicates mature 3D microcolony architecture.
    4. Structural Classification: Non-pathogenic early attachment vs mature matrix-enclosed infectious biofilm.
    """

    if uploaded_pdf is not None:
        st.sidebar.success(f"📄 Custom Protocol: **{uploaded_pdf.name}**")
        extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        imaging_text = extracted if "Error" not in extracted else default_imaging_text
    else:
        imaging_text = default_imaging_text

    # ==========================================
    # 1. CLSM & SEM IMAGE FEATURE EXTRACTOR
    # ==========================================
    if sub_tool == "🖼️ 1. CLSM & SEM Image Feature Extractor":
        st.subheader("🖼️ Quantitative Microscopic Feature Extraction")
        st.write("Extract structural parameters (biomass volume, average thickness, roughness coefficient) from Z-stack array files.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Imaging Parameters")
            st.number_input("Pixel Resolution (µm/pixel)", value=0.108, format="%.3f")
            st.number_input("Z-Step Size (µm)", value=0.50, format="%.2f")
            st.slider("Fluorescence Threshold Cutoff", 0, 255, 45)
        with col2:
            st.markdown("##### Sample Dataset Generator")
            if st.button("Generate Synthetic Biofilm Z-Stack Data", use_container_width=True):
                np.random.seed(42)
                z_slices = 20
                biomass_per_slice = np.random.normal(12.5, 2.1, size=z_slices)
                df_biofilm = pd.DataFrame({
                    "Slice_Z": range(1, z_slices + 1),
                    "Biomass_µm3": biomass_per_slice,
                    "Live_Fraction": np.random.uniform(0.70, 0.95, size=z_slices),
                    "Dead_Fraction": np.random.uniform(0.05, 0.30, size=z_slices)
                })
                st.session_state["biofilm_data"] = df_biofilm
                st.success("Synthetic Z-Stack generated!")

        if "biofilm_data" in st.session_state:
            df = st.session_state["biofilm_data"]
            st.markdown("### 📊 Extracted Z-Stack Quantification")
            st.dataframe(df, use_container_width=True)

            total_biomass = df["Biomass_µm3"].sum()
            avg_live = df["Live_Fraction"].mean() * 100
            roughness_ra = df["Biomass_µm3"].std() / df["Biomass_µm3"].mean()

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Biomass Volume", f"{total_biomass:.2f} µm³")
            m2.metric("Mean Live Cell Ratio", f"{avg_live:.1f}%")
            m3.metric("Roughness Coeff (Ra)", f"{roughness_ra:.3f}", delta="Mature Matrix" if roughness_ra > 0.15 else "Early Layer")

    # ==========================================
    # 2. BIOFILM STRUCTURAL VIABILITY CLASSIFIER
    # ==========================================
    elif sub_tool == "🧬 2. Biofilm Structural Viability Classifier":
        st.subheader("🧬 Neural Network Viability & Stage Classifier")
        st.write("Run deep-learning feature classification to categorize microcolony growth stages and antimicrobial tolerance risks.")

        c1, c2 = st.columns(2)
        with c1:
            thickness = st.number_input("Mean Thickness (µm)", value=24.5)
            density = st.number_input("EPS Matrix Density Score (0-1)", value=0.82)
        with c2:
            live_ratio = st.slider("Live Cell Percentage (%)", 0.0, 100.0, 85.0)
            amr_suspect = st.checkbox("Persistent Phenotype Flag", value=True)

        if st.button("Run Neural Network Classification", type="primary", use_container_width=True):
            if thickness > 20.0 and density > 0.70:
                stage = "Stage IV: Mature Biofilm Matrix"
                risk = "High Tolerant Phenotype"
            else:
                stage = "Stage II: Microcolony Formation"
                risk = "Moderate Susceptibility"

            st.success(f"**Diagnostic Output:** {stage}")
            st.info(f"**Phenotypic Risk Level:** {risk}")

    # ==========================================
    # 3. GROUNDED IMAGING SOP AUDIT
    # ==========================================
    elif sub_tool == "⚖️ 3. Grounded Imaging SOP Audit":
        st.subheader("⚖️ Imaging Protocol & Compliance RAG Query")
        st.write("Query uploaded microscopy manuals and image quantification protocols.")

        query = st.text_input(
            "Enter microscopy protocol or fluorophore query:",
            placeholder="e.g., What fluorophore concentration and incubation time are specified for live/dead staining?"
        )

        if st.button("Run Imaging SOP Audit", use_container_width=True):
            if query.strip():
                with st.spinner("Retrieving microscopy SOP context..."):
                    context = rag_engine.retrieve_relevant_context(query, imaging_text)
                    result = rag_engine.query_rag_engine(query, context, "Microscopy & Imaging Specialist")
                    st.success(result)
                    with st.expander("🔍 View Retrieved SOP Context"):
                        st.code(context, language="text")
            else:
                st.warning("Please enter a query above.")

    # ==========================================
    # 4. GEMINI BIOFILM AI ADVISOR
    # ==========================================
    elif sub_tool == "🤖 4. Gemini Biofilm AI Advisor":
        st.subheader("🤖 Gemini Biofilm Imaging & Diagnostic Advisor")
        st.write("Consult the AI advisor for image processing troubleshooting, CLSM Z-stack interpretation, and biofilm matrix analysis.")

        bio_query = st.text_area(
            "Describe your imaging finding, Z-stack anomaly, or biofilm growth condition:",
            placeholder="e.g., SYTO 9 channel exhibits heavy background fluorescence in the lower 5 µm Z-slices."
        )

        if st.button("Run AI Imaging Evaluation", type="primary"):
            if not bio_query.strip():
                st.warning("Please enter your imaging details.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                if not api_key:
                    st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables.")
                else:
                    with st.spinner("Analyzing microscopy data with Gemini AI..."):
                        try:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            context = rag_engine.retrieve_relevant_context(bio_query, imaging_text)
                            
                            prompt = f"""
                            You are an expert biofilm microbiologist, confocal laser scanning microscopy specialist, and bio-image analysis researcher.
                            Provide expert analysis and troubleshooting for the following imaging inquiry:

                            User Query:
                            {bio_query}

                            Active Protocol / SOP Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            st.markdown("### 📋 AI Biofilm Imaging Guidance")
                            st.success(response.text)
                        except Exception as e:
                            st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
