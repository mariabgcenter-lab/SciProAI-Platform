import os
import google.generativeai as genai
import numpy as np
import pandas as pd
import streamlit as st
import modules.rag_engine as rag_engine


def main():
    st.title("🧫 Biocontrol & Antimicrobial Inhibition Suite (`biocontrol_inhibition`)")
    st.markdown("""
    Research module for evaluating antimicrobial susceptibility, broth microdilution (MIC/MBC), 
    biofilm eradication concentration (MBEC), combination synergy (FIC index), and biocontrol efficacy, backed by Gemini AI.
    """)

    st.markdown("---")

    # Sub-Navigation Menu
    sub_tool = st.radio(
        "Select Biocontrol Module:",
        [
            "🧪 1. Broth Microdilution & MIC / MBC Calculator",
            "🧫 2. Zone of Inhibition & MBEC Profiler",
            "🔀 3. Combination Synergy & FIC Index",
            "⚖️ 4. Grounded Biocontrol Protocol Audit",
            "🤖 5. Gemini Biocontrol AI Advisor",
        ],
        horizontal=True,
    )

    st.markdown("---")

    # Sidebar PDF Protocol Intake for Grounded RAG
    st.sidebar.header("📁 Biocontrol SOP Intake")
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload Biocontrol SOP / AST Protocol (PDF)", 
        type=["pdf"], 
        help="Upload CLSI M100 guidelines, EUCAST breakpoints, or biocontrol testing protocols."
    )

    default_biocontrol_text = """
    Biocontrol & Antimicrobial Susceptibility Testing (AST) Knowledge Base:
    1. Minimum Inhibitory Concentration (MIC): Lowest agent concentration that completely inhibits visible growth (OD600 < 0.05).
    2. Minimum Bactericidal Concentration (MBC): Lowest concentration yielding ≥ 99.9% (3-log10) reduction in viable CFU/mL.
    3. Fractional Inhibitory Concentration (FIC) Index: 
       - FIC <= 0.5: Synergistic interaction.
       - 0.5 < FIC <= 1.0: Additive interaction.
       - 1.0 < FIC <= 4.0: Indifferent / No interaction.
       - FIC > 4.0: Antagonistic interaction.
    4. Biofilm Eradication: Minimum Biofilm Eradication Concentration (MBEC) typically 10x to 1000x higher than planktonic MIC due to EPS matrix barrier.
    """

    if uploaded_pdf is not None:
        st.sidebar.success(f"📄 Custom Protocol: **{uploaded_pdf.name}**")
        extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        biocontrol_text = extracted if "Error" not in extracted else default_biocontrol_text
    else:
        biocontrol_text = default_biocontrol_text

    # ==========================================
    # 1. BROTH MICRODILUTION & MIC / MBC CALCULATOR
    # ==========================================
    if sub_tool == "🧪 1. Broth Microdilution & MIC / MBC Calculator":
        st.subheader("🧪 Broth Microdilution & Minimum Inhibitory Concentration (MIC)")
        st.write("Calculate percent bacterial growth inhibition across serial 2-fold dilution series.")

        col1, col2 = st.columns(2)
        with col1:
            control_od = st.number_input("Growth Control OD600 (Untreated)", value=0.850, format="%.3f")
            blank_od = st.number_input("Sterile Media Blank OD600", value=0.045, format="%.3f")
        with col2:
            agent_name = st.text_input("Antimicrobial / Biocontrol Agent Name", value="Phage Cocktail BC-01")
            stock_conc = st.number_input("Highest Tested Conc (µg/mL or MOI)", value=128.0)

        st.markdown("##### Serial 2-Fold Dilution OD600 Input")
        dilutions = [stock_conc / (2**i) for i in range(8)]
        od_inputs = []
        cols = st.columns(4)
        for idx, conc in enumerate(dilutions):
            with cols[idx % 4]:
                od_val = st.number_input(f"{conc:.2f} µg/mL OD", value=float(np.round(0.048 + 0.1 * (idx**1.5) / 10, 3)), key=f"od_{idx}")
                od_inputs.append(od_val)

        if st.button("Calculate MIC & % Inhibition", type="primary", use_container_width=True):
            net_control = max(0.001, control_od - blank_od)
            inhibition_list = []
            mic_found = None

            for conc, raw_od in zip(dilutions, od_inputs):
                net_sample = max(0.0, raw_od - blank_od)
                pct_inh = max(0.0, min(100.0, (1.0 - (net_sample / net_control)) * 100.0))
                inhibition_list.append(pct_inh)
                if pct_inh >= 95.0 and mic_found is None:
                    mic_found = conc

            df_mic = pd.DataFrame({
                "Concentration (µg/mL)": dilutions,
                "Measured OD600": od_inputs,
                "Inhibition (%)": np.round(inhibition_list, 2)
            })

            st.markdown("### 📊 Serial Dilution Results")
            st.dataframe(df_mic, use_container_width=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("Agent Tested", agent_name)
            m2.metric("Estimated MIC", f"{mic_found:.2f} µg/mL" if mic_found else "> Highest Conc")
            m3.metric("Max Inhibition", f"{max(inhibition_list):.1f}%")

    # ==========================================
    # 2. ZONE OF INHIBITION & MBEC PROFILER
    # ==========================================
    elif sub_tool == "🧫 2. Zone of Inhibition & MBEC Profiler":
        st.subheader("🧫 Disk Diffusion Zone & Biofilm Eradication (MBEC)")
        st.write("Profile agar disk diffusion clearance zones and evaluate planktonic MIC vs biofilm MBEC tolerance shift.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Disk Diffusion Measurements")
            zone_mm = st.number_input("Inhibition Zone Diameter (mm)", value=21.5, format="%.1f")
            clsi_susceptible = st.number_input("CLSI Susceptible Cutoff (≥ mm)", value=18.0)
            clsi_resistant = st.number_input("CLSI Resistant Cutoff (≤ mm)", value=14.0)
        with c2:
            st.markdown("##### Biofilm Matrix Resistance Shift")
            planktonic_mic = st.number_input("Planktonic MIC (µg/mL)", value=4.0)
            biofilm_mbec = st.number_input("Biofilm MBEC (µg/mL)", value=256.0)

        if st.button("Evaluate Susceptibility & Biofilm Protection Index", type="primary"):
            if zone_mm >= clsi_susceptible:
                ast_category = "Susceptible (S)"
                badge_color = "normal"
            elif zone_mm <= clsi_resistant:
                ast_category = "Resistant (R)"
                badge_color = "inverse"
            else:
                ast_category = "Intermediate (I)"
                badge_color = "off"

            fold_increase = biofilm_mbec / max(0.001, planktonic_mic)

            k1, k2, k3 = st.columns(3)
            k1.metric("AST Phenotype", ast_category, delta="Clearance Validated")
            k2.metric("Planktonic vs MBEC Shift", f"{fold_increase:.1f}x Fold Resistance")
            k3.metric("Matrix Protection Rating", "Extremely High" if fold_increase >= 50 else "Moderate Protection")

    # ==========================================
    # 3. COMBINATION SYNERGY & FIC INDEX
    # ==========================================
    elif sub_tool == "🔀 3. Combination Synergy & FIC Index":
        st.subheader("🔀 Combination Synergy & Fractional Inhibitory Concentration (FIC)")
        st.write("Calculate FIC index for combination therapy (e.g., Antibiotic + Biocontrol Peptide / Enzyme).")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("##### Agent A (e.g., Standard Antibiotic)")
            mic_a_alone = st.number_input("MIC of Agent A Alone (µg/mL)", value=16.0)
            mic_a_combo = st.number_input("MIC of Agent A in Combination (µg/mL)", value=2.0)
        with col_b:
            st.markdown("##### Agent B (e.g., Biocontrol / Enzyme / Phage)")
            mic_b_alone = st.number_input("MIC of Agent B Alone (µg/mL)", value=64.0)
            mic_b_combo = st.number_input("MIC of Agent B in Combination (µg/mL)", value=8.0)

        if st.button("Calculate FIC Index & Interaction Category", type="primary", use_container_width=True):
            fic_a = mic_a_combo / max(0.0001, mic_a_alone)
            fic_b = mic_b_combo / max(0.0001, mic_b_alone)
            fic_index = fic_a + fic_b

            if fic_index <= 0.5:
                interpretation = "Synergistic (FIC ≤ 0.5)"
                status_fn = st.success
            elif fic_index <= 1.0:
                interpretation = "Additive (0.5 < FIC ≤ 1.0)"
                status_fn = st.info
            elif fic_index <= 4.0:
                interpretation = "Indifferent (1.0 < FIC ≤ 4.0)"
                status_fn = st.warning
            else:
                interpretation = "Antagonistic (FIC > 4.0)"
                status_fn = st.error

            s1, s2, s3 = st.columns(3)
            s1.metric("FIC Component A", f"{fic_a:.3f}")
            s2.metric("FIC Component B", f"{fic_b:.3f}")
            s3.metric("Total FIC Index", f"{fic_index:.3f}")

            status_fn(f"**Combination Interaction Outcome:** {interpretation}")

    # ==========================================
    # 4. GROUNDED BIOCONTROL PROTOCOL AUDIT
    # ==========================================
    elif sub_tool == "⚖️ 4. Grounded Biocontrol Protocol Audit":
        st.subheader("⚖️ Biocontrol SOP & AST Guidelines RAG Audit")
        st.write("Cross-examine inhibition protocols and AST thresholds against uploaded SOPs.")

        query = st.text_input(
            "Enter biocontrol or AST query:",
            placeholder="e.g., What is the definition threshold for bactericidal activity (MBC) vs bacteriostatic activity?"
        )

        if st.button("Run Protocol Audit Query", use_container_width=True):
            if query.strip():
                with st.spinner("Retrieving biocontrol protocol context..."):
                    context = rag_engine.retrieve_relevant_context(query, biocontrol_text)
                    result = rag_engine.query_rag_engine(query, context, "Antimicrobial & Biocontrol Specialist")
                    st.success(result)
                    with st.expander("🔍 View Retrieved Context Snippets"):
                        st.code(context, language="text")
            else:
                st.warning("Please enter a query above.")

    # ==========================================
    # 5. GEMINI BIOCONTROL AI ADVISOR
    # ==========================================
    elif sub_tool == "🤖 5. Gemini Biocontrol AI Advisor":
        st.subheader("🤖 Gemini Biocontrol & AST AI Advisor")
        st.write("Consult the AI advisor for assistance with experimental formulation, biofilm degradation, and combination antimicrobial synergy.")

        bio_query = st.text_area(
            "Describe your biocontrol challenge, MIC anomaly, or combination assay finding:",
            placeholder="e.g., We observed a 4-fold decrease in MIC when pairing essential oils with endolysins against P. aeruginosa."
        )

        if st.button("Run AI Biocontrol Evaluation", type="primary"):
            if not bio_query.strip():
                st.warning("Please enter your biocontrol query.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                if not api_key:
                    st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables.")
                else:
                    with st.spinner("Analyzing biocontrol data with Gemini AI..."):
                        try:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            context = rag_engine.retrieve_relevant_context(bio_query, biocontrol_text)

                            prompt = f"""
                            You are an expert microbiologist, antimicrobial susceptibility testing (AST) specialist, and biocontrol formulation scientist.
                            Provide thorough, professional analysis and recommendations for the following inquiry:

                            User Query:
                            {bio_query}

                            Active Protocol / SOP Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            st.markdown("### 📋 AI Biocontrol & AST Guidance")
                            st.success(response.text)
                        except Exception as e:
                            st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
