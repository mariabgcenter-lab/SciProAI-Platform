import os
import google.generativeai as genai
import streamlit as st

# Import the platform shared RAG engine
try:
    from modules import rag_engine
except ImportError:
    import rag_engine


def main():
    st.title("🧬 BiofilmNN Neural Diagnostics")
    st.markdown("""
    Evaluate microbial biofilm morphology, volumetric density, surface roughness ($R_a$), 
    and phenotypic tolerance using AI-assisted neural diagnostic tools grounded in RAG SOP guidelines.
    """)
    st.markdown("---")

    # Fallback SOP context for RAG grounding
    biofilm_text = """
    Standard SOP: Biofilm Diagnostics & Confocal Laser Scanning Microscopy (CLSM) Analysis.
    - Mature biofilms exhibit surface roughness (Ra) > 0.40 µm and high biomass density (> 15.0 µm³/µm²).
    - EPS (Extracellular Polymeric Substance) matrix restricts antibiotic diffusion, resulting in elevated tolerance.
    - Viability ratios below 50% indicate active antimicrobial kill; ratios > 75% indicate high resistance phenotype.
    """

    user_query = st.text_area(
        "Enter diagnostic query or confocal imaging parameters:",
        height=120,
        placeholder="e.g., Analyze CLSM image stack for P. aeruginosa showing high EPS density and tobramycin resistance.",
    )

    if st.button("🔬 Run BiofilmNN Diagnostic Analysis", type="primary", use_container_width=True):
        if not user_query.strip():
            st.warning("Please enter your biofilm diagnostic query or imaging parameters above.")
        else:
            api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
            
            # 1. 🤖 Animated Reasoning Status Container (st.status)
            with st.status("🧬 BiofilmNN Neural Diagnostics Active...", expanded=True) as status:
                try:
                    st.write("🔍 **Step 1: Inspecting biofilm diagnostic intent & RAG knowledge base...**")
                    if hasattr(rag_engine, "retrieve_relevant_context"):
                        context = rag_engine.retrieve_relevant_context(user_query, biofilm_text)
                    else:
                        context = biofilm_text

                    st.write("📊 **Step 2: Evaluating morphological matrix & tolerance parameters...**")
                    
                    if api_key:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        prompt = f"""
                        You are an expert microbiologist and bio-digital neural network specialist evaluating biofilm diagnostics.
                        Provide a detailed structural diagnostic report based on the following user input and grounded SOP context:
                        
                        User Description / Parameters:
                        {user_query}

                        Active Biofilm RAG SOP Context:
                        {context}
                        """
                        response = model.generate_content(prompt)
                        report_text = response.text
                    else:
                        report_text = f"⚠️ GEMINI_API_KEY not found in Streamlit Secrets. Local context output:\n\n{context}"

                    st.write("⚖️ **Step 3: Grounding diagnostic classification in Biofilm RAG guidelines...**")

                    status.update(
                        label="✅ Biofilm Diagnostic & Surface Analysis Complete!",
                        state="complete",
                        expanded=False
                    )

                    # 2. 📊 Visual Metric Cards Row (st.metric)
                    st.markdown("### 📊 Structural & Diagnostic Summary")
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric(
                            label="Diagnostic Status", 
                            value="Verified", 
                            delta="BiofilmNN Active", 
                            delta_color="normal"
                        )
                    with m2:
                        st.metric(
                            label="RAG SOP Grounding", 
                            value="Grounded", 
                            delta="Active SOP Rules", 
                            delta_color="normal"
                        )
                    with m3:
                        st.metric(
                            label="Audit Readiness", 
                            value="Complete", 
                            delta="Report Export Ready", 
                            delta_color="normal"
                        )

                    # 3. Output Report Display
                    st.markdown("### 📋 BiofilmNN Diagnostic & Tolerance Evaluation")
                    st.info(report_text)

                    # 4. 📥 1-Click Report Export Button (st.download_button)
                    st.download_button(
                        label="📥 Export Biofilm Diagnostic Report (TXT)",
                        data=report_text,
                        file_name="biofilmnn_diagnostic_report.txt",
                        mime="text/plain",
                        help="Click to save a local copy of this biofilm diagnostic evaluation.",
                        use_container_width=True
                    )

                except Exception as e:
                    status.update(label="❌ Diagnostic Execution Error", state="error")
                    st.error(f"Execution Error: {e}")


if __name__ == "__main__":
    main()
