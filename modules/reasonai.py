import streamlit as st

def main():
    # ---------------------------------------------------------
    # PAGE CONFIGURATION
    # ---------------------------------------------------------
    st.set_page_config(
        page_title="ReasonAI — LLM Reasoning Evaluator",
        layout="wide"
    )

    st.title("🧠 ReasonAI — LLM Reasoning Evaluator")
    st.write("""
    Evaluate the **quality, logic, and correctness** of AI-generated reasoning  
    for scientific, regulatory, and laboratory workflows.
    """)

    # ---------------------------------------------------------
    # SIDEBAR NAVIGATION
    # ---------------------------------------------------------
    st.sidebar.header("ReasonAI Modules")
    module = st.sidebar.radio(
        "Select a module:",
        [
            "Reasoning Quality Scoring",
            "Stepwise Logic Checker",
            "Regulatory Alignment Review"
        ]
    )

    # ---------------------------------------------------------
    # MODULE 1 — Reasoning Quality Scoring
    # ---------------------------------------------------------
    if module == "Reasoning Quality Scoring":
        st.subheader("📊 Reasoning Quality Scoring")

        text = st.text_area("Paste AI-generated reasoning:")

        if st.button("Score Reasoning"):
            if not text.strip():
                st.warning("Please paste reasoning text.")
            else:
                # Simple illustrative scoring
                length_score = min(len(text) / 200, 1.0)
                clarity_score = 0.8
                logic_score = 0.85
                domain_score = 0.9

                final_score = (length_score + clarity_score + logic_score + domain_score) / 4

                st.write("### Reasoning Scores")
                st.json({
                    "Clarity": clarity_score,
                    "Logical Flow": logic_score,
                    "Domain Alignment": domain_score,
                    "Completeness": length_score,
                    "Final Score": round(final_score, 2)
                })

    # ---------------------------------------------------------
    # MODULE 2 — Stepwise Logic Checker
    # ---------------------------------------------------------
    if module == "Stepwise Logic Checker":
        st.subheader("🔁 Stepwise Logic Checker")

        st.write("Paste stepwise instructions to evaluate logical consistency.")

        steps = st.text_area("Stepwise instructions (one step per line):")

        if st.button("Check Logic"):
            if not steps.strip():
                st.warning("Please enter stepwise instructions.")
            else:
                step_list = [s.strip() for s in steps.split("\n") if s.strip()]

                st.write("### Stepwise Logic Review")
                for i, step in enumerate(step_list, start=1):
                    st.write(f"**Step {i}:** {step}")

                st.write("""
                **Logic Evaluation (Illustrative):**
                - Steps appear sequential  
                - No contradictory actions detected  
                - No missing prerequisite steps detected  
                """)

    # ---------------------------------------------------------
    # MODULE 3 — Regulatory Alignment Review
    # ---------------------------------------------------------
    if module == "Regulatory Alignment Review":
        st.subheader("📑 Regulatory Alignment Review")

        text = st.text_area("Paste AI-generated SOP, QC note, or validation text:")

        framework = st.selectbox(
            "Regulatory Framework:",
            ["CLIA", "CAP", "ISO 17025"]
        )

        if st.button("Evaluate Alignment"):
            if not text.strip():
                st.warning("Please paste text for evaluation.")
            else:
                st.write("### Regulatory Alignment Summary")
                st.write(f"**Framework:** {framework}")

                st.write("""
                **Alignment Indicators (Illustrative):**
                - Structure resembles required documentation format  
                - Terminology consistent with regulatory expectations  
                - No major compliance gaps detected  
                - Recommend human review for final approval  
                """)
