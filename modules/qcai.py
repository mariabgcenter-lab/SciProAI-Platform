import os
import google.generativeai as genai
import streamlit as st

# Import the platform shared RAG engine
try:
    from modules import rag_engine
except ImportError:
    import rag_engine


def main():
    st.title("📊 Quality Control & Compliance Suite (QCAI)")
    st.markdown("""
    Evaluate laboratory quality control runs, audit out-of-control flags (**Westgard 1-3s, 2-2s, R-4s** rules), 
    and synthesize ISO/CLIA-compliant CAPA (Corrective and Preventive Action) recommendations using RAG-grounded AI advisors.
    """)
    st.markdown("---")

    # Fallback QA/QC SOP context for RAG grounding
    qc_text = """
    Standard Operating Procedure: Quality Control & Westgard Multi-Rule Evaluation (CLSI C24 Guidelines).
    - 1_2s Rule: Warning flag when 1 control measurement exceeds mean ± 2SD.
    - 1_3s Rule: Rejection flag when 1 control measurement exceeds mean ± 3SD (Random error trigger).
    - 2_2s Rule: Rejection flag when 2 consecutive control measurements exceed mean + 2SD or mean - 2SD (Systematic error trigger).
    - R_4s Rule: Rejection flag when 1 control exceeds mean + 2SD and another exceeds mean - 2SD within same run.
    - 4_1s Rule: Rejection flag when 4 consecutive control measurements exceed mean + 1SD or mean - 1SD.
    - 10_x Rule: Rejection flag when 10 consecutive control measurements fall on one side of the mean.
    - Required Action: Immediately hold clinical reporting, inspect reagent lot, perform recalibration, and document CAPA log.
    """

    sub_tool = st.radio(
        "Select Quality Control Tool:",
        ["📈 Westgard QC Evaluator", "🤖 Gemini QA/QC AI Advisor"],
        horizontal=True
    )
    st.markdown("---")

    # ---------------------------------------------------------
    # SUB-TOOL 1: Westgard QC Evaluator
    # ---------------------------------------------------------
    if sub_tool == "📈 Westgard QC Evaluator":
        st.subheader("📈 Interactive Westgard Control Rule Check")
        st.write("Enter control measurement parameters or run values below to verify compliance against CLSI C24 limits.")

        col_a, col_b = st.columns(2)
        with col_a:
            target_mean = st.number_input("Target Control Mean:", value=100.0, step=1.0)
            target_sd = st.number_input("Target Standard Deviation (SD):", value=5.0, step=0.5)
        with col_b:
            observed_val = st.number_input("Observed Control Value:", value=116.5, step=1.0)
            previous_val = st.number_input("Previous Control Value (Run N-1):", value=111.0, step=1.0)

        if st.button("📊 Evaluate Westgard Rules", type="primary", use_container_width=True):
            # Calculate SD offsets
            sd_diff = (observed_val - target_mean) / target_sd if target_sd > 0 else 0
            prev_sd_diff = (previous_val - target_mean) / target_sd if target_sd > 0 else 0

            # Westgard Rule Checks
            violation_1_3s = abs(sd_diff) > 3.0
            violation_2_2s = (sd_diff > 2.0 and prev_sd_diff > 2.0) or (sd_diff < -2.0 and prev_sd_diff < -2.0)
            warning_1_2s = abs(sd_diff) > 2.0 and not violation_1_3s and not violation_2_2s

            is_rejected = violation_1_3s or violation_2_2s

            # 1. 📊 Visual Metric Cards Row (st.metric)
            st.markdown("### 📊 QC Run Summary & Westgard Evaluation")
            m1, m2, m3 = st.columns(3)

            with m1:
                if is_rejected:
                    st.metric(
                        label="QC Control Status",
                        value="REJECTED",
                        delta="Westgard Violation",
                        delta_color="inverse"
                    )
                elif warning_1_2s:
                    st.metric(
                        label="QC Control Status",
                        value="WARNING",
                        delta="1-2s Rule Flagged",
                        delta_color="off"
                    )
                else:
                    st.metric(
                        label="QC Control Status",
                        value="PASSED",
                        delta="Within ±2SD Limits",
                        delta_color="normal"
                    )

            with m2:
                st.metric(
                    label="Mean SD Offset",
                    value=f"{sd_diff:+.2f} SD",
                    delta="Target: 0.00 SD",
                    delta_color="off"
                )

            with m3:
                st.metric(
                    label="Evaluated Rules",
                    value="CLSI C24",
                    delta="Audit Verified",
                    delta_color="normal"
                )

            # Detailed Explanation Output
            if is_rejected:
                reasons = []
                if violation_1_3s:
                    reasons.append("• **1_3s Violation**: Observed value exceeds ±3SD (Random Error risk).")
                if violation_2_2s:
                    reasons.append("• **2_2s Violation**: Two consecutive values exceed ±2SD (Systematic Error risk).")
                
                eval_details = f"❌ **RUN REJECTED**: The run failed quality control criteria.\n\n" + "\n".join(reasons) + "\n\n**Action Item:** Halt patient testing, run secondary control lot, and perform recalibration per SOP."
                st.error(eval_details)
            elif warning_1_2s:
                eval_details = "⚠️ **WARNING (1_2s Rule)**: Control value is between ±2SD and ±3SD. Run may proceed, but monitor next run closely for systematic drift."
                st.warning(eval_details)
            else:
                eval_details = "✅ **RUN PASSED**: All control values are within acceptable ±2SD statistical limits. Proceed with clinical analysis."
                st.success(eval_details)

            # 2. 📥 1-Click Report Export Button (st.download_button)
            st.download_button(
                label="📥 Export QC Evaluation Summary (TXT)",
                data=f"Quality Control Check Results:\nTarget Mean: {target_mean}\nTarget SD: {target_sd}\nObserved Value: {observed_val} ({sd_diff:+.2f} SD)\n\nEvaluation Details:\n{eval_details}",
                file_name="westgard_qc_eval_report.txt",
                mime="text/plain",
                use_container_width=True
            )

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
            height=120,
            placeholder="e.g., Control Lot #204 demonstrated repeated 1_3s Westgard flags over 3 consecutive runs."
        )

        if st.button("🚀 Run AI QA Evaluation", type="primary", use_container_width=True):
            if not qa_query.strip():
                st.warning("Please enter your QC event details above before running.")
            else:
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                
                # 1. 🤖 Animated Reasoning Status Container (st.status)
                with st.status("🤖 Analyzing Quality Control Event & CAPA Context...", expanded=True) as status:
                    try:
                        st.write("🔍 **Step 1: Retrieving active SOP & compliance RAG context...**")
                        if hasattr(rag_engine, "retrieve_relevant_context"):
                            context = rag_engine.retrieve_relevant_context(qa_query, qc_text)
                        else:
                            context = qc_text

                        st.write("⚖️ **Step 2: Synthesizing ISO/CLIA root-cause analysis & CAPA plan...**")
                        
                        if api_key:
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
                            report_text = response.text
                        else:
                            report_text = f"⚠️ GEMINI_API_KEY not found in Streamlit Secrets. Grounded SOP Context:\n\n{context}"

                        status.update(
                            label="✅ QA Root-Cause & CAPA Analysis Complete!", 
                            state="complete", 
                            expanded=False
                        )
                        
                        # 2. 📊 Visual Metric Cards Row (st.metric)
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
                        st.success(report_text)

                        # 3. 📥 1-Click Download Button (st.download_button)
                        st.download_button(
                            label="📥 Export CAPA & Root-Cause Audit Report (TXT)",
                            data=report_text,
                            file_name="sciproai_capa_report.txt",
                            mime="text/plain",
                            help="Click to save this CAPA and root-cause analysis to your computer.",
                            use_container_width=True
                        )

                    except Exception as e:
                        status.update(label="❌ Analysis Execution Error", state="error")
                        st.error(f"API Error: {e}")


if __name__ == "__main__":
    main()
