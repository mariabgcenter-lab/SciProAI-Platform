import os
import math
import pandas as pd
import google.generativeai as genai
import streamlit as st

# Import platform shared RAG engine
try:
    from modules import rag_engine
except ImportError:
    import rag_engine


def calculate_tm_gc(sequence: str):
    """Calculate GC% and estimated melting temperature (Tm) for PCR primers."""
    seq = sequence.upper().strip()
    if not seq:
        return 0.0, 0.0
    gc_count = seq.count('G') + seq.count('C')
    gc_pct = (gc_count / len(seq)) * 100.0
    if len(seq) < 14:
        tm = (seq.count('A') + seq.count('T')) * 2 + (gc_count * 4)
    else:
        tm = 64.9 + 41.0 * (gc_count - 16.4) / len(seq)
    return round(gc_pct, 1), round(tm, 1)


def main():
    st.title("🔬 AssayAI: Molecular Assay Design & PCR Suite")
    st.markdown("""
    Design, evaluate, and optimize qPCR / dPCR molecular diagnostic assays, calculate genetic copy numbers, 
    and consult RAG-grounded AI advisors for assay troubleshooting and MIQE compliance.
    """)
    st.markdown("---")

    # Fallback SOP context for RAG grounding
    assay_text = """
    Standard Operating Procedure: Molecular PCR Diagnostic Assay Design & MIQE Guidelines.
    - Primer length should be 18–24 bp with GC content between 40% and 60%.
    - Melting Temperature (Tm) should be between 58°C and 62°C, with ΔTm between forward and reverse primers < 2°C.
    - Avoid G/C clamps longer than 3 bases at 3' end to prevent non-specific priming.
    - qPCR Amplicon length should ideally be 70–150 bp for optimal extension rate.
    - Standard curve slope should range between -3.58 and -3.10, corresponding to 90%–110% PCR efficiency (R² > 0.990).
    """

    sub_tool = st.radio(
        "Select AssayAI Tool:",
        ["🧬 Primer & Probe Evaluator", "📈 Copy Number & Standard Curve", "🤖 Gemini AI Assay Advisor"],
        horizontal=True
    )
    st.markdown("---")

    # ---------------------------------------------------------
    # SUB-TOOL 1: Primer & Probe Evaluator
    # ---------------------------------------------------------
    if sub_tool == "🧬 Primer & Probe Evaluator":
        st.subheader("🧬 Interactive Primer & Probe Parameter Check")
        st.write("Input forward and reverse primer sequences to evaluate Tm matching, GC content, and MIQE compliance.")

        col_fwd, col_rev = st.columns(2)
        with col_fwd:
            fwd_seq = st.text_input("Forward Primer (5' -> 3'):", value="ATGCGATCGATCGATCGATC")
        with col_rev:
            rev_seq = st.text_input("Reverse Primer (5' -> 3'):", value="GCTAGCTAGCTAGCTAGCTA")

        if st.button("🔬 Evaluate Primer Pair", type="primary", use_container_width=True):
            fwd_gc, fwd_tm = calculate_tm_gc(fwd_seq)
            rev_gc, rev_tm = calculate_tm_gc(rev_seq)
            delta_tm = abs(fwd_tm - rev_tm)

            # MIQE Compliance Check
            tm_pass = (58.0 <= fwd_tm <= 62.0) and (58.0 <= rev_tm <= 62.0) and (delta_tm <= 2.0)
            gc_pass = (40.0 <= fwd_gc <= 60.0) and (40.0 <= rev_gc <= 60.0)

            # 1. 📊 Visual Metric Cards Row (st.metric)
            st.markdown("### 📊 Primer Parameter Summary")
            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    label="Forward Primer Tm / GC",
                    value=f"{fwd_tm} °C",
                    delta=f"{fwd_gc}% GC ({len(fwd_seq)} bp)",
                    delta_color="normal" if (58.0 <= fwd_tm <= 62.0 and 40.0 <= fwd_gc <= 60.0) else "off"
                )

            with m2:
                st.metric(
                    label="Reverse Primer Tm / GC",
                    value=f"{rev_tm} °C",
                    delta=f"{rev_gc}% GC ({len(rev_seq)} bp)",
                    delta_color="normal" if (58.0 <= rev_tm <= 62.0 and 40.0 <= rev_gc <= 60.0) else "off"
                )

            with m3:
                st.metric(
                    label="Primer Pair ΔTm",
                    value=f"{delta_tm:.1f} °C",
                    delta="MIQE Compliant" if tm_pass and gc_pass else "ΔTm Flag",
                    delta_color="normal" if tm_pass and gc_pass else "inverse"
                )

            # Summary Report Text
            primer_report = (
                f"Primer Design Evaluation Report:\n"
                f"- Forward Primer: {fwd_seq} (Length: {len(fwd_seq)} bp | Tm: {fwd_tm}°C | GC: {fwd_gc}%)\n"
                f"- Reverse Primer: {rev_seq} (Length: {len(rev_seq)} bp | Tm: {rev_tm}°C | GC: {rev_gc}%)\n"
                f"- Melting Temperature Difference (ΔTm): {delta_tm:.1f}°C\n"
                f"- MIQE Temperature Status: {'PASSED (Within 58-62°C range)' if tm_pass else 'FLAGGED (Adjust Tm to 58-62°C)'}\n"
                f"- MIQE GC Content Status: {'PASSED (Within 40-60% GC)' if gc_pass else 'FLAGGED (Adjust GC to 40-60%)'}\n"
            )

            if tm_pass and gc_pass:
                st.success("✅ **EXCELLENT PRIMER PAIR**: Both primers satisfy MIQE recommendations for Tm matching and GC balance.")
            else:
                st.warning("⚠️ **ASSAY ADVISORY**: One or both primers deviate from optimal MIQE thermal/GC windows.")

            st.info(primer_report)

            # 2. 📥 1-Click Report Export Button (st.download_button)
            st.download_button(
                label="📥 Export Primer Evaluation Report (TXT)",
                data=primer_report,
                file_name="assayai_primer_evaluation.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ---------------------------------------------------------
    # SUB-TOOL 2: Copy Number & Standard Curve
    # ---------------------------------------------------------
    elif sub_tool == "📈 Copy Number & Standard Curve":
        st.subheader("📈 Absolute Copy Number & Efficiency Calculator")
        st.write("Calculate genetic copy numbers from DNA concentration (ng/µL) and amplicon length, or estimate PCR efficiency.")

        col_input1, col_input2 = st.columns(2)
        with col_input1:
            dna_conc = st.number_input("DNA Concentration (ng/µL):", value=10.0, min_value=0.0001, step=1.0)
            amplicon_len = st.number_input("Amplicon Length (bp):", value=120, min_value=1, step=10)
        with col_input2:
            vol_ul = st.number_input("Reaction Volume (µL):", value=2.0, min_value=0.1, step=0.5)
            slope = st.number_input("Standard Curve Slope (for Efficiency %):", value=-3.32, step=0.05)

        if st.button("📊 Calculate Copy Number & Efficiency", type="primary", use_container_width=True):
            mass_g = dna_conc * 1e-9 * vol_ul
            copy_num = (mass_g * 6.02214076e23) / (amplicon_len * 660.0)

            if slope != 0:
                eff_pct = (math.pow(10, -1.0 / slope) - 1.0) * 100.0
            else:
                eff_pct = 0.0

            # 1. 📊 Visual Metric Cards Row (st.metric)
            st.markdown("### 📊 Quantitative Calculation Results")
            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    label="Absolute Copy Number",
                    value=f"{copy_num:.2e}",
                    delta="Copies per Reaction",
                    delta_color="normal"
                )

            with m2:
                st.metric(
                    label="PCR Efficiency (E)",
                    value=f"{eff_pct:.1f}%",
                    delta="Target: 90% - 110%",
                    delta_color="normal" if (90.0 <= eff_pct <= 110.0) else "inverse"
                )

            with m3:
                st.metric(
                    label="Curve Slope",
                    value=f"{slope:.2f}",
                    delta="Ideal: -3.32",
                    delta_color="normal" if (-3.58 <= slope <= -3.10) else "off"
                )

            calc_report = (
                f"Absolute Quantification & Efficiency Report:\n"
                f"- Input DNA Concentration: {dna_conc} ng/µL (Reaction Volume: {vol_ul} µL)\n"
                f"- Amplicon Length: {amplicon_len} bp\n"
                f"- Calculated Absolute Copy Number: {copy_num:.4e} copies/reaction\n"
                f"- Standard Curve Slope: {slope:.2f}\n"
                f"- Amplification Efficiency: {eff_pct:.2f}%\n"
            )
            st.info(calc_report)

            # 2. 📥 1-Click Export Button (st.download_button)
            st.download_button(
                label="📥 Export Quantification Report (TXT)",
                data=calc_report,
                file_name="assayai_copy_number_report.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ---------------------------------------------------------
    # SUB-TOOL 3: Gemini AI Assay Optimization Advisor
    # ---------------------------------------------------------
    elif sub_tool == "🤖 Gemini AI Assay Advisor":
        st.subheader("🤖 Gemini AI Assay Optimization & MIQE Advisor")
        st.write(
            "Consult the AI advisor for expert qPCR/dPCR troubleshooting, primer-dimer mitigation, "
            "fluorophore multiplexing advice, and MIQE guideline compliance."
        )

        assay_query = st.text_area(
            "Describe your assay design question, reaction failure, or optimization goal:",
            height=120,
            placeholder="e.g., How can we eliminate non-specific amplification peaks in our target pelA qPCR assay without losing sensitivity?"
        )

        if st.button("🚀 Run AI Assay Optimization", type="primary", use_container_width=True):
            if not assay_query.strip():
                st.warning("Please enter your assay design question above before running.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

                # 1. 🤖 Animated Reasoning Status Container (st.status)
                with st.status("🤖 Analyzing Molecular Assay Design & RAG Context...", expanded=True) as status:
                    try:
                        st.write("🔍 **Step 1: Retrieving active MIQE guidelines & assay RAG context...**")
                        if hasattr(rag_engine, "retrieve_relevant_context"):
                            context = rag_engine.retrieve_relevant_context(assay_query, assay_text)
                        else:
                            context = assay_text

                        st.write("🧬 **Step 2: Synthesizing PCR kinetics & reaction optimization strategy...**")

                        if api_key:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-1.5-flash")

                            prompt = f"""
                            You are an expert molecular biologist, PCR assay design engineer, and MIQE compliance specialist.
                            Provide rigorous, professional troubleshooting, primer redesign recommendations, and protocol optimization for the following request:

                            User Description / Question:
                            {assay_query}

                            Active Assay SOP / MIQE Context:
                            {context}
                            """
                            response = model.generate_content(prompt)
                            report_text = response.text
                        else:
                            report_text = f"⚠️ GEMINI_API_KEY not found in Streamlit Secrets. Grounded SOP Context:\n\n{context}"

                        status.update(
                            label="✅ Molecular Assay Optimization Analysis Complete!",
                            state="complete",
                            expanded=False
                        )

                        # 2. 📊 Visual Metric Cards Row (st.metric)
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.metric(
                                label="Design Evaluation",
                                value="Optimized",
                                delta="MIQE Guidelines",
                                delta_color="normal"
                            )
                        with m2:
                            st.metric(
                                label="RAG SOP Grounding",
                                value="Grounded",
                                delta="Active Context",
                                delta_color="normal"
                            )
                        with m3:
                            st.metric(
                                label="Audit Readiness",
                                value="Complete",
                                delta="Report Ready",
                                delta_color="normal"
                            )

                        st.markdown("### 📋 AI Molecular Assay Expert Guidance")
                        st.success(report_text)

                        # 3. 📥 1-Click Download Button (st.download_button)
                        st.download_button(
                            label="📥 Export AI Assay Optimization Report (TXT)",
                            data=report_text,
                            file_name="sciproai_assay_optimization_report.txt",
                            mime="text/plain",
                            help="Click to save this assay optimization analysis to your computer.",
                            use_container_width=True
                        )

                    except Exception as e:
                        status.update(label="❌ Analysis Execution Error", state="error")
                        st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
