import streamlit as st

st.title("🧪 SOP & Protocol Summary Assistant")

st.write(
    "Summarizes SOPs, protocols, and step-by-step workflows to provide a clear overview of "
    "what the document contains and what the experiment is about."
)

st.markdown("---")

# ---------------------------------------------------------
# File Upload Section
# ---------------------------------------------------------
st.subheader("📄 Upload SOP or Protocol Document")

uploaded_file = st.file_uploader(
    "Upload SOP or protocol (PDF, TXT, DOCX)",
    type=["pdf", "txt", "docx"]
)

sop_text = ""

# ---------------------------------------------------------
# Extract Text from Uploaded File
# ---------------------------------------------------------
if uploaded_file:

    # PDF extraction
    if uploaded_file.type == "application/pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            sop_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            st.error("Unable to read PDF file.")

    # TXT extraction
    elif uploaded_file.type == "text/plain":
        try:
            sop_text = uploaded_file.read().decode("utf-8")
        except Exception:
            st.error("Unable to read TXT file.")

    # DOCX extraction
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            import docx
            doc = docx.Document(uploaded_file)
            sop_text = "\n".join([para.text for para in doc.paragraphs])
        except Exception:
            st.error("Unable to read DOCX file.")

# ---------------------------------------------------------
# Fallback Manual Paste
# ---------------------------------------------------------
st.subheader("📄 Or Paste SOP/Protocol Text")

manual_text = st.text_area(
    "Paste SOP or protocol here:",
    height=300,
    placeholder="Paste your SOP/protocol text..."
)

# If upload succeeded, use uploaded text; otherwise use manual text
if sop_text.strip() == "":
    sop_text = manual_text

st.markdown("---")

# ---------------------------------------------------------
# Summary Button
# ---------------------------------------------------------
if st.button("Generate SOP Summary", type="primary"):
    st.markdown("### 📝 SOP Summary")

    if len(sop_text.strip()) == 0:
        st.warning("Please upload or paste SOP text before summarizing.")
    else:
        # Simple section extraction
        sections = {
            "Purpose": ["purpose", "objective", "goal"],
            "Materials": ["materials", "reagents", "supplies"],
            "Equipment": ["equipment", "instruments", "tools"],
            "Procedure": ["procedure", "steps", "protocol"],
            "Conditions": ["conditions", "temperature", "incubation", "timing"],
            "Safety": ["safety", "hazards", "ppe"],
            "Expected Results": ["results", "outcome", "observation"]
        }

        lower_sop = sop_text.lower()

        for title, keywords in sections.items():
            st.markdown(f"#### {title}")
            extracted = []

            for kw in keywords:
                if kw in lower_sop:
                    extracted.append(kw)

            if extracted:
                st.write(f"Section detected based on keywords: {', '.join(extracted)}")
                st.write("Summary:")
                st.write(f"- This SOP contains information related to **{title.lower()}**.")
            else:
                st.write("No explicit section detected.")
            st.markdown("---")

        st.success("SOP summary generated.")
