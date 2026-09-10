import streamlit as st
import re

# ---------------------------------------------------------
# Module Header
# ---------------------------------------------------------
st.title("📘 Scientific Document Summary Module")

st.write(
    "Summarizes scientific documents—including methods, workflows, technical notes, and "
    "publications—to extract the main purpose, experimental context, and key scientific "
    "content. Provides a concise overview of what the document contains and what the "
    "study or experiment is about."
)

st.markdown("---")

# ---------------------------------------------------------
# File Upload Section
# ---------------------------------------------------------
st.subheader("📄 Upload Scientific Document")

uploaded_doc = st.file_uploader(
    "Upload document (PDF, TXT, DOCX)",
    type=["pdf", "txt", "docx"]
)

doc_text = ""

# ---------------------------------------------------------
# Extract Text from Uploaded File
# ---------------------------------------------------------
if uploaded_doc:

    # PDF extraction
    if uploaded_doc.type == "application/pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_doc)
            doc_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            st.error("Unable to read PDF file.")

    # TXT extraction
    elif uploaded_doc.type == "text/plain":
        try:
            doc_text = uploaded_doc.read().decode("utf-8")
        except Exception:
            st.error("Unable to read TXT file.")

    # DOCX extraction
    elif uploaded_doc.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            import docx
            doc = docx.Document(uploaded_doc)
            doc_text = "\n".join([para.text for para in doc.paragraphs])
        except Exception:
            st.error("Unable to read DOCX file.")

# ---------------------------------------------------------
# Fallback Manual Paste
# ---------------------------------------------------------
st.subheader("📄 Or Paste Document Text")

manual_text = st.text_area(
    "Paste scientific document text:",
    height=300,
    placeholder="Paste methods, workflow, or scientific text..."
)

# If upload succeeded, use uploaded text; otherwise use manual text
if doc_text.strip() == "":
    doc_text = manual_text

st.markdown("---")

# ---------------------------------------------------------
# Summarization Button
# ---------------------------------------------------------
if st.button("Generate Summary", type="primary"):
    st.markdown("### 🧪 Scientific Document Summary")

    if len(doc_text.strip()) == 0:
        st.warning("Please upload or paste document text before generating a summary.")
    else:
        # Clean text
        clean_text = re.sub(r"\s+", " ", doc_text.strip())

        # Extract first 3–5 sentences as a simple scientific summary
        sentences = re.split(r'(?<=[.!?]) +', clean_text)
        summary = " ".join(sentences[:5])

        st.write(summary)

        st.markdown("---")

        # Keyword extraction (simple scientific term frequency)
        words = re.findall(r"\b[A-Za-z]{5,}\b", clean_text.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1

        top_keywords = sorted(freq, key=freq.get, reverse=True)[:10]

        st.markdown("### 🔬 Key Scientific Terms")
        st.write(", ".join(top_keywords))
