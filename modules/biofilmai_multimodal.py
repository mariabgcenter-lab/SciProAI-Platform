import os
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import filters, io, measure, morphology, segmentation
import streamlit as st


def main():
  # ---------------------------------------------------------
  # PAGE CONFIGURATION (Handled globally by app.py)
  # ---------------------------------------------------------

  st.title("🔬 BiofilmAI — Multimodal Biofilm Modeling Suite")
  st.write("""
    This suite integrates **gene expression analysis**, **microscopy image processing**,  
    **multimodal fusion**, and **AI-powered research summarization** into a unified scientific workflow.
    """)

  # ---------------------------------------------------------
  # SIDEBAR NAVIGATION
  # ---------------------------------------------------------
  st.sidebar.header("BiofilmAI Modules")
  module = st.sidebar.radio(
      "Select a module:",
      [
          "Gene Expression Checker",
          "Biofilm Image Analyzer",
          "Multimodal Fusion Hub",
          "Research Document Summary",
          "🤖 Gemini Multimodal AI Advisor",
      ],
  )

  # ---------------------------------------------------------
  # MODULE 1 — Gene Expression Checker
  # ---------------------------------------------------------
  if module == "Gene Expression Checker":
    st.subheader("🧬 Gene Expression Checker")

    uploaded = st.file_uploader(
        "Upload differential expression CSV", type=["csv", "tsv"]
    )

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Preview")
      st.dataframe(df.head())

      # Volcano plot
      if "log_FC" in df.columns and "deseq.p-value" in df.columns:
        st.write("### Volcano Plot")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df["log_FC"], -np.log10(df["deseq.p-value"]), s=10, alpha=0.6)
        ax.set_xlabel("log2 Fold Change")
        ax.set_ylabel("-log10(p-value)")
        ax.set_title("Volcano Plot")
        st.pyplot(fig)

      else:
        st.warning("Required columns not found: log_FC, deseq.p-value")

  # ---------------------------------------------------------
  # MODULE 2 — Biofilm Image Analyzer
  # ---------------------------------------------------------
  elif module == "Biofilm Image Analyzer":
    st.subheader("🧫 Biofilm Image Analyzer")

    uploaded_img = st.file_uploader(
        "Upload microscopy image", type=["png", "jpg", "jpeg"]
    )

    if uploaded_img:
      img = io.imread(uploaded_img)
      st.image(img, caption="Uploaded Image", use_column_width=True)

      # Convert to grayscale
      if img.ndim == 3:
        gray = np.mean(img, axis=2)
      else:
        gray = img

      # Segmentation
      blurred = filters.gaussian(gray, sigma=1.0)
      thresh = filters.threshold_otsu(blurred)
      binary = blurred > thresh
      cleaned = morphology.remove_small_objects(binary, min_size=50)

      # Watershed
      distance = ndi.distance_transform_edt(cleaned)
      local_maxi = morphology.local_maxima(distance)
      markers = measure.label(local_maxi)
      labels = segmentation.watershed(-distance, markers, mask=cleaned)

      st.write("### Segmentation Result")
      fig, ax = plt.subplots(figsize=(8, 6))
      ax.imshow(labels, cmap="nipy_spectral")
      ax.set_title("Watershed Segmentation")
      ax.axis("off")
      st.pyplot(fig)

      st.write("### Object Count:", labels.max())

  # ---------------------------------------------------------
  # MODULE 3 — Multimodal Fusion Hub
  # ---------------------------------------------------------
  elif module == "Multimodal Fusion Hub":
    st.subheader("🧪 Multimodal Fusion Hub")

    st.write("""
        Combine **gene expression embeddings** and **image embeddings**  
        to create unified multimodal predictions.
        """)

    expr_file = st.file_uploader(
        "Upload gene expression feature table", type=["csv"]
    )
    img_file = st.file_uploader("Upload image feature table", type=["csv"])

    if expr_file and img_file:
      expr = pd.read_csv(expr_file)
      img = pd.read_csv(img_file)

      st.write("### Gene Expression Features")
      st.dataframe(expr.head())

      st.write("### Image Features")
      st.dataframe(img.head())

      # Simple fusion example
      st.write("### Early Fusion Example")
      fused = pd.concat([expr, img], axis=1)
      st.dataframe(fused.head())

  # ---------------------------------------------------------
  # MODULE 4 — Research Document Summary (Upgraded with Gemini API)
  # ---------------------------------------------------------
  elif module == "Research Document Summary":
    st.subheader("📄 AI-Powered Research Document Summary")
    st.write(
        "Paste scientific text, abstracts, or notes below to generate a"
        " structured AI summary using Gemini 1.5-flash."
    )

    text = st.text_area("Paste scientific text to summarize:")

    if st.button("Generate AI Summary", type="primary"):
      if len(text.strip()) == 0:
        st.warning("Please paste scientific text first.")
      else:
        api_key = st.secrets.get(
            "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")
        )
        if not api_key:
          st.error(
              "⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment"
              " Variables."
          )
        else:
          with st.spinner("Synthesizing scientific literature..."):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert scientific literature reviewer and microbiologist. 
                            Provide a structured, rigorous summary of the following text, highlighting key biological findings, 
                            methodology, and implications for biofilm research:
                            {text}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 Structured Scientific Summary")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")

  # ---------------------------------------------------------
  # MODULE 5 — Gemini Multimodal AI Advisor
  # ---------------------------------------------------------
  elif module == "🤖 Gemini Multimodal AI Advisor":
    st.subheader("🤖 Multimodal Biofilm AI Advisor")
    st.write(
        "Ask questions combining gene expression profiles, microscopic"
        " features, or biofilm architecture for cross-domain insights."
    )

    multimodal_query = st.text_area("Enter your research question or notes:")

    if st.button("Run AI Analysis", type="primary"):
      if not multimodal_query.strip():
        st.warning("Please enter a research query.")
      else:
        api_key = st.secrets.get(
            "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")
        )
        if not api_key:
          st.error(
              "⚠️ GEMINI_API_KEY not found in Streamlit Secrets or Environment"
              " Variables."
          )
        else:
          with st.spinner("Analyzing multimodal parameters..."):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert computational biologist specializing in multi-omics and biofilm imaging analytics. 
                            Provide professional insights on the following research inquiry:
                            {multimodal_query}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 Expert Multimodal Synthesis")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")
