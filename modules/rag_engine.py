import os
import PyPDF2
import streamlit as st

try:
  import google.generativeai as genai

  HAS_GENAI = True
except ImportError:
  HAS_GENAI = False


def extract_text_from_pdf(file_stream) -> str:
  """Extracts raw text content from uploaded PDF files."""
  try:
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
      extracted = page.extract_text()
      if extracted:
        text += extracted + "\n"
    return text
  except Exception as e:
    return f"Error extracting text: {e}"


def retrieve_relevant_context(
    query: str, text_content: str, chunk_size: int = 600, top_k: int = 3
) -> str:
  """Splits document text into chunks and returns top matching snippets."""
  chunks = [
      text_content[i : i + chunk_size]
      for i in range(0, len(text_content), chunk_size)
  ]
  query_words = set(query.lower().split())

  scored_chunks = []
  for chunk in chunks:
    score = sum(1 for word in query_words if word in chunk.lower())
    if score > 0:
      scored_chunks.append((score, chunk))

  scored_chunks.sort(key=lambda x: x[0], reverse=True)
  top_chunks = [chunk for score, chunk in scored_chunks[:top_k]]

  if top_chunks:
    return "\n\n--- [RETRIEVED CONTEXT] ---\n\n".join(top_chunks)
  return text_content[:1800]


def query_rag_engine(query: str, context: str, domain_role: str) -> str:
  """Executes Gemini 1.5 Flash query grounded strictly in retrieved context."""
  api_key = st.secrets.get(
      "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")
  )

  if HAS_GENAI and api_key:
    try:
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel("gemini-1.5-flash")

      prompt = f"""
            You are an expert {domain_role}.
            Answer the user query strictly using the retrieved context provided below. Cite specific sections, numbers, or rules where applicable.

            User Query: {query}

            Retrieved Context:
            {context}
            """

      response = model.generate_content(prompt)
      return response.text
    except Exception as e:
      return f"⚠️ Gemini RAG Error: {e}"

  return (
      f"📄 **Simulated RAG Analysis ({domain_role}):**\n- Query processed:"
      f" '{query}'.\n- Retrieved relevant knowledge chunks grounded in uploaded"
      " documents."
  )
