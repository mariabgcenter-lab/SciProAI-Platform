import os
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import modules.rag_engine as rag_engine


def main():
    st.title("📊 Diagnostic & Biofilm Analytics Dashboards (`dashboards_visualization`)")
    st.markdown("""
    Interactive commercial analytics suite for monitoring polymicrobial biofilm growth dynamics, 
    multi-site assay quality control trends, matrix diffusion heatmaps, and grounded executive reporting, backed by Gemini AI.
    """)

    st.markdown("---")

    # Sub-Navigation Menu
    sub_tool = st.radio(
        "Select Dashboard Module:",
        [
            "📈 1. Polymicrobial Community Dynamics Dashboard",
            "🏢 2. Multi-Site QC & Assay Trend Dashboard",
            "🧫 3. Matrix Diffusion & AMR Heatmap Visualizer",
            "⚖️ 4. Grounded Analytics RAG Report Query",
            "🤖 5. Gemini Dashboard AI Advisor",
        ],
        horizontal=True,
    )

    st.markdown("---")

    # Sidebar PDF Report Intake for Grounded RAG
    st.sidebar.header("📁 Analytics SOP Intake")
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload Analytics / Trend Report (PDF)", 
        type=["pdf"], 
        help="Upload multi-site QC reports, clinical trial summaries, or biofilm trend SOPs."
    )

    default_dash_text = """
    Biofilm & Clinical Diagnostic Dashboard Knowledge Base:
    1. Polymicrobial Dynamics: Co-culture shift toward >70% P. aeruginosa dominance signals mature competitive matrix state.
    2. Multi-Site Quality Control: Westgard 1-3s rule violation triggers immediate run rejection across clinical testing nodes.
    3. Matrix Permeability Heatmap: Antimicrobial penetration depth < 15 µm indicates high structural biofilm resistance.
    4. Compliance KPI: Facility pass rate threshold set to ≥ 95.0% for all operational diagnostic lines.
    """

    if uploaded_pdf is not None:
        st.sidebar.success(f"📄 Custom Report: **{uploaded_pdf.name}**")
        extracted = rag_engine.extract_text_from_pdf(uploaded_pdf)
        dash_text = extracted if "Error" not in extracted else default_dash_text
    else:
        dash_text = default_dash_text

    # ==========================================
    # 1. POLYMICROBIAL COMMUNITY DYNAMICS DASHBOARD
    # ==========================================
    if sub_tool == "📈 1. Polymicrobial Community Dynamics Dashboard":
        st.subheader("📈 Polymicrobial Co-Culture Growth Dynamics")
        st.write("Track species ratios, biomass volume accumulation, and competitive shifts across time points.")

        c1, c2 = st.columns(2)
        with c1:
            species_a = st.text_input("Primary Species A:", value="Pseudomonas aeruginosa")
            species_b = st.text_input("Secondary Species B:", value="Staphylococcus aureus")
        with c2:
            time_hours = st.slider("Time Course Duration (Hours)", 6, 72, 48, step=6)
            growth_temp = st.selectbox("Incubation Temperature:", ["37°C (Physiological)", "30°C (Environmental)", "25°C (Room Temp)"])

        if st.button("Generate Growth Dynamics Dashboard", type="primary", use_container_width=True):
            np.random.seed(42)
            time_points = np.arange(0, time_hours + 1, 6)
            pop_a = 1e4 * np.exp(0.12 * time_points) + np.random.normal(0, 500, len(time_points))
            pop_b = 1e4 * np.exp(0.08 * time_points) + np.random.normal(0, 300, len(time_points))

            df_growth = pd.DataFrame({
                "Time_Hours": time_points,
                f"{species_a} (CFU/mL)": np.round(pop_a, 0),
                f"{species_b} (CFU/mL)": np.round(pop_b, 0),
                "Total_Biomass_Index": np.round((pop_a + pop_b) / 1000.0, 2)
            })

            st.markdown("### 📊 Population Growth & Ratio Dataset")
            st.dataframe(df_growth, use_container_width=True)

            final_a = pop_a[-1]
            final_b = pop_b[-1]
            ratio_a = (final_a / (final_a + final_b)) * 100

            k1, k2, k3 = st.columns(3)
            k1.metric(f"Final {species_a}", f"{final_a:,.0f} CFU/mL")
            k2.metric(f"Final {species_b}", f"{final_b:,.0f} CFU/mL")
            k3.metric("Species A Dominance", f"{ratio_a:.1f}% Ratio", delta="Competitive Shift" if ratio_a > 60 else "Balanced")

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(time_points, pop_a, "o-", label=species_a, color="#1f77b4", linewidth=2)
            ax.plot(time_points, pop_b, "s-", label=species_b, color="#ff7f0e", linewidth=2)
            ax.set_xlabel("Time (Hours)")
            ax.set_ylabel("Population Density (CFU/mL)")
            ax.set_title("Co-Culture Population Kinetics")
            ax.set_yscale("log")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend()
            st.pyplot(fig)

    # ==========================================
    # 2. MULTI-SITE QC & ASSAY TREND DASHBOARD
    # ==========================================
    elif sub_tool == "🏢 2. Multi-Site QC & Assay Trend Dashboard":
        st.subheader("🏢 Multi-Site Clinical Quality Control Monitor")
        st.write("Monitor assay run performance, Levey-Jennings control limits, and Westgard rule compliance across diagnostic sites.")

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            target_mean = st.number_input("Target Control Mean", value=100.0, format="%.1f")
            target_sd = st.number_input("Target Control SD", value=5.0, format="%.1f")
        with col_q2:
            num_runs = st.slider("Audited Run Count", 10, 50, 20)
            site_name = st.selectbox("Clinical Site:", ["Central Molecular Hub - USA", "Regional Clinical Node - EU", "Validation Lab - Asia"])

        if st.button("Generate Levey-Jennings Trend Audit", type="primary", use_container_width=True):
            np.random.seed(101)
            run_vals = np.random.normal(target_mean, target_sd, num_runs)
            ucl_3sd = target_mean + (3 * target_sd)
            lcl_3sd = target_mean - (3 * target_sd)

            violations = [i + 1 for i, v in enumerate(run_vals) if v > ucl_3sd or v < lcl_3sd]

            df_qc = pd.DataFrame({
                "Run_ID": range(1, num_runs + 1),
                "Control_Value": np.round(run_vals, 2),
                "Z_Score": np.round((run_vals - target_mean) / target_sd, 2),
                "Status": ["REJECT (1-3s)" if v in violations else "ACCEPT" for v in range(1, num_runs + 1)]
            })

            st.markdown("### 📊 Levey-Jennings Quality Control Audit Table")
            st.dataframe(df_qc, use_container_width=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("Site Name", site_name.split("-")[0].strip())
            m2.metric("Total Audited Runs", f"{num_runs}")
            m3.metric(
                "Westgard Pass Rate", 
                f"{((num_runs - len(violations)) / num_runs) * 100:.1f}%",
                delta="Compliant" if len(violations) == 0 else f"{len(violations)} Violation(s)",
                delta_color="normal" if len(violations) == 0 else "inverse"
            )

    # ==========================================
    # 3. MATRIX DIFFUSION & AMR HEATMAP VISUALIZER
    # ==========================================
    elif sub_tool == "🧫 3. Matrix Diffusion & AMR Heatmap Visualizer":
        st.subheader("🧫 Antimicrobial Matrix Penetration & Phenotype Heatmap")
        st.write("Visualize drug penetration efficiency across spatial matrix depths and bacterial strains.")

        st.markdown("##### Matrix Heatmap Controls")
        strains = ["P. aeruginosa WT", "P. aeruginosa ΔalgD", "S. aureus MRSA", "K. pneumoniae KPC", "A. baumannii CR"]
        drugs = ["Tobramycin", "Ciprofloxacin", "Meropenem", "Colistin", "Vancomycin"]

        if st.button("Generate Matrix Penetration Heatmap", type="primary", use_container_width=True):
            np.random.seed(7)
            matrix_data = np.random.uniform(15.0, 98.0, size=(len(strains), len(drugs)))

            df_heatmap = pd.DataFrame(matrix_data, index=strains, columns=drugs)

            st.markdown("### 📊 Matrix Penetration Efficiency (%)")
            st.dataframe(df_heatmap.style.background_gradient(cmap="Blues"), use_container_width=True)

            avg_pen = matrix_data.mean()
            min_pen = matrix_data.min()

            h1, h2 = st.columns(2)
            h1.metric("Mean Penetration Efficiency", f"{avg_pen:.1f}%")
            h2.metric("Lowest Penetration Barrier", f"{min_pen:.1f}%", delta="High Diffusion Barrier", delta_color="inverse")

    # ==========================================
    # 4. GROUNDED ANALYTICS RAG REPORT QUERY
    # ==========================================
    elif sub_tool == "⚖️ 4. Grounded Analytics RAG Report Query":
        st.subheader("⚖️ Executive Analytics & SOP RAG Audit Query")
        st.write("Query uploaded multi-site clinical trial reports, quality metrics, and performance SOPs.")

        query = st.text_input(
            "Enter dashboard or analytics query:",
            placeholder="e.g., What is the acceptable Westgard QC pass rate threshold and competitive dominance cutoff?"
        )

        if st.button("Run Analytics RAG Audit Query", use_container_width=True):
            if query.strip():
                with st.spinner("Retrieving analytics report context..."):
                    context = rag_engine.retrieve_relevant_context(query, dash_text)
                    result = rag_engine.query_rag_engine(query, context, "Clinical Analytics & Quality Systems Specialist")
                    st.success(result)
                    with st.expander("🔍 View Retrieved Context Snippets"):
                        st.code(context, language="text")
            else:
                st.warning("Please enter a query above.")

    # ==========================================
    # 5. GEMINI DASHBOARD AI ADVISOR
    # ==========================================
    elif sub_tool == "🤖 5. Gemini Dashboard AI Advisor":
        st.subheader("🤖 Gemini Diagnostic Analytics & Dashboard Advisor")
        st.write("Consult the AI advisor for trend interpretations, quality control troubleshooting, and clinical KPI optimization.")

        dash_query = st.text_area(
            "Describe your analytics challenge, out-of-control QC run, or population kinetics query:",
            placeholder="e.g., Central Node site reports a consistent +2.2 SD shift in control values over the past 5 operational days."
        )

        if st.button("Run AI Analytics Evaluation", type="primary"):
            if not dash_query.strip():
                st.warning("Please enter your query details.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                if not api_key:
                    st.error("⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables.")
                else:
                    with st.spinner("Analyzing dashboard metrics with Gemini AI..."):
                        try:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            context = rag_engine.retrieve_relevant_context(dash_query, dash_text)

                            prompt = f"""
                            You are an expert clinical laboratory director, quality systems manager, and bio-analytics specialist.
                            Provide clear, actionable recommendations for the following diagnostic analytics inquiry:

                            User Inquiry:
                            {dash_query}

                            Active Report / Protocol Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            st.markdown("### 📋 AI Analytics & Quality Guidance")
                            st.success(response.text)
                        except Exception as e:
                            st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
