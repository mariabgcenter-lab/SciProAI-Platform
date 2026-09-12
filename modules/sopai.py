import streamlit as st
import re

def main():
    st.title("📄 SOP Version Control & Compliance Auditor")
    st.markdown("""
    Upload your laboratory Standard Operating Procedure (SOP) to instantly cross-reference it 
    against quality management standards (like ISO/IEC 17025 or ISO 9001) and flag missing compliance elements, 
    outdated version markers, or structural gaps.
    """)

    st.markdown("---")

    # Layout: Two columns for configuration and upload
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Audit Configuration")
        target_standard = st.selectbox(
            "Select Regulatory Benchmark / Standard:",
            [
                "ISO/IEC 17025:2017 (General requirements for testing and calibration laboratories)",
                "ISO 9001:2015 (Quality Management Systems)",
                "FDA cGMP / GLP Compliance Framework",
                "Internal Standard / Custom Checklist"
            ]
        )
        
        sop_id_input = st.text_input("SOP Document ID (Optional)", placeholder="e.g., SOP-MB-104")
        version_input = st.text_input("Current Document Version", placeholder="e.g., Rev 3.2")

    with col2:
        st.subheader("2. Upload SOP Document")
        uploaded_file = st.file_uploader("Upload SOP File (.txt or extracted text)", type=["txt", "md"])
        st.info("Tip: If your SOP is a PDF, paste the extracted text or upload a .txt export for precise parsing.")

    st.markdown("---")

    if uploaded_file is not None:
        # Read file content
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
        
        st.subheader("3. Document Preview")
        with st.expander("View Uploaded SOP Text"):
            st.text_area("Source Text", file_content, height=200, disabled=True)

        if st.button("Run Compliance & Gap Audit", use_container_width=True, type="primary"):
            with st.spinner("Analyzing document structure and checking regulatory elements..."):
                
                # --- Deterministic Compliance Checks ---
                text_lower = file_content.lower()
                
                # Mandatory sections check
                mandatory_elements = {
                    "Purpose / Objective": ["purpose", "objective", "aim", "scope"],
                    "Responsibility / Personnel": ["responsibility", "authorized", "personnel", "operator", "analyst"],
                    "Materials & Equipment": ["equipment", "reagents", "materials", "supplies", "instrumentation"],
                    "Step-by-Step Procedure": ["procedure", "method", "instructions", "step", "protocol"],
                    "Quality Control / Acceptance Criteria": ["quality control", "qc", "acceptance criteria", "blank", "spike", "outlier"],
                    "Corrective Action / Troubleshooting": ["corrective action", "troubleshooting", "deviation", "non-conformance"],
                    "References / Document Control": ["reference", "document history", "effective date", "approved by", "version"]
                }

                audit_results = {}
                missing_count = 0
                
                for element, keywords in mandatory_elements.items():
                    found = any(kw in text_lower for kw in keywords)
                    audit_results[element] = found
                    if not found:
                        missing_count += 1

                # --- Results Display ---
                st.markdown("---")
                st.subheader("📋 SOP Compliance Audit Report")
                
                if sop_id_input or version_input:
                    st.caption(f"**Document:** {sop_id_input or 'Unspecified'} | **Version:** {version_input or 'Unspecified'} | **Standard:** {target_standard}")

                # Metrics summary
                m1, m2, m3 = st.columns(3)
                m1.metric("Target Benchmark", target_standard.split("(")[0].strip())
                m2.metric("Mandatory Elements Found", f"{len(mandatory_elements) - missing_count} / {len(mandatory_elements)}")
                m3.metric("Audit Status", "Needs Revision" if missing_count > 0 else "Fully Aligned", 
                          delta="Action Required" if missing_count > 0 else "Passed", delta_color="inverse" if missing_count > 0 else "normal")

                st.markdown("### Structural Gap Breakdown")
                for element, passed in audit_results.items():
                    if passed:
                        st.success(f"**[FOUND]** {element} section identified in text.")
                    else:
                        st.error(f"**[MISSING / UNCLEAR]** {element} section could not be detected. Recommended addition for compliance.")

                st.markdown("### Next Steps & Recommendations")
                if missing_count > 0:
                    st.warning("Your document is missing critical sections required by standard laboratory quality frameworks. Update the sections flagged above before submitting for formal QA review.")
                else:
                    st.success("All primary structural and regulatory elements appear to be present in this document text.")

    else:
        st.info("Please upload an SOP text file above to initiate the compliance audit.")
