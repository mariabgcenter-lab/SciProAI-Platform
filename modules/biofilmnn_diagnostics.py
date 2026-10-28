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

  st.title("🧫 BiofilmNN — AI Diagnostics Suite")
  st.write("""
    This suite provides **AI-assisted microbial diagnostics**, including image-based classification,  
    AMR (antimicrobial resistance) feature extraction, segmentation previews, and AI-powered diagnostic reasoning.
    """)

  # ---------------------------------------------------------
  # SIDEBAR NAVIGATION
  # ---------------------------------------------------------
  st.sidebar.header("BiofilmNN Modules")
  module = st.sidebar.radio(
      "Select a module:",
      [
          "Microbial Image Diagnostics",
          "AMR Prediction (AMRAI)",
          "Image Feature Extraction",
          "Diagnostic Reasoning Preview",
          "🤖 Gemini Diagnostics AI Advisor",
      ],
  )

  # ---------------------------------------------------------
  # MODULE 1 — Microbial Image Diagnostics
  # ---------------------------------------------------------
  if module == "Microbial Image Diagnostics":
    st.subheader("🔬 Microbial Image Diagnostics")

    uploaded_img = st.file_uploader(
        "Upload microbial microscopy image", type=["png", "jpg", "jpeg"]
    )

    if uploaded_img:
      img = io.imread(uploaded_img)
      st.image(img, caption="Uploaded Image", use_column_width=True)

      # Convert to grayscale
      if img.ndim == 3:
        gray = np.mean(img, axis=2)
      else:
        gray = img

      # Basic segmentation
      blurred = filters.gaussian(gray, sigma=1.0)
      thresh = filters.threshold_otsu(blurred)
      binary = blurred > thresh
      cleaned = morphology.remove_small_objects(binary, min_size=50)

      # Watershed segmentation
      distance = ndi.distance_transform_edt(cleaned)
      local_maxi = morphology.local_maxima(distance)
      markers = measure.label(local_maxi)
      labels = segmentation.watershed(-distance, markers, mask=cleaned)

      st.write("### Segmentation Result")
      fig, ax = plt.subplots(figsize=(8, 6))
      ax.imshow(labels, cmap="nipy_spectral")
      ax.set_title("Microbial Segmentation")
      ax.axis("off")
      st.pyplot(fig)

      st.write("### Object Count:", labels.max())

  # ---------------------------------------------------------
  # MODULE 2 — AMR Prediction (AMRAI)
  # ---------------------------------------------------------
  elif module == "AMR Prediction (AMRAI)":
    st.subheader("🧪 AMRAI — Antimicrobial Resistance Prediction")

    st.write("""
        Upload AMR-related gene expression or phenotype tables  
        to preview antimicrobial resistance indicators.
        """)

    uploaded = st.file_uploader("Upload AMR dataset (CSV)", type=["csv"])

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      # Simple AMR scoring example
      if "gene" in df.columns and "expression" in df.columns:
        df["AMR_score"] = df["expression"].apply(lambda x: np.log2(x + 1))
        st.write("### AMR Score Table")
        st.dataframe(df[["gene", "AMR_score"]])
      else:
        st.warning("Required columns not found: gene, expression")

  # ---------------------------------------------------------
  # MODULE 3 — Image Feature Extraction
  # ---------------------------------------------------------
  elif module == "Image Feature Extraction":
    st.subheader("📊 Image Feature Extraction")

    uploaded_img = st.file_uploader(
        "Upload image for feature extraction", type=["png", "jpg", "jpeg"]
    )

    if uploaded_img:
      img = io.imread(uploaded_img)
      st.image(img, caption="Uploaded Image", use_column_width=True)

      # Convert to grayscale
      if img.ndim == 3:
        gray = np.mean(img, axis=2)
      else:
        gray = img

      # Feature extraction
      mean_intensity = np.mean(gray)
      std_intensity = np.std(gray)
      max_intensity = np.max(gray)
      min_intensity = np.min(gray)

      st.write("### Extracted Features")
      st.json({
          "Mean Intensity": float(mean_intensity),
          "Std Intensity": float(std_intensity),
          "Max Intensity": float(max_intensity),
          "Min Intensity": float(min_intensity),
      })

  # ---------------------------------------------------------
  # MODULE 4 — Diagnostic Reasoning Preview (Upgraded with Gemini API)
  # ---------------------------------------------------------
  elif module == "Diagnostic Reasoning Preview":
    st.subheader("🧠 AI-Powered Diagnostic Reasoning")
    st.write(
        "Describe the microbial sample, clinical presentation, or diagnostic"
        " findings to generate a structured AI evaluation via Gemini"
        " 1.5-flash."
    )

    text = st.text_area("Describe the microbial sample or diagnostic question:")

    if st.button("Generate Diagnostic Reasoning", type="primary"):
      if len(text.strip()) == 0:
        st.warning("Please enter a description first.")
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
          with st.spinner("Analyzing diagnostic parameters..."):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert clinical microbiologist and specialist in biofilm-associated infections and antimicrobial resistance. 
                            Provide a rigorous, professional diagnostic evaluation and actionable recommendations based on the following observations:
                            {text}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 AI Diagnostic Evaluation")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")

  # ---------------------------------------------------------
  # MODULE 5 — Gemini Diagnostics AI Advisor
  # ---------------------------------------------------------
  elif module == "🤖 Gemini Diagnostics AI Advisor":
    st.subheader("🤖 BiofilmNN Expert AI Advisor")
    st.write(
        "Consult the AI advisor for specialized inquiries regarding microbial"
        " imaging metrics, AMR phenotypes, and advanced diagnostic workflows."
    )

    diagnostics_query = st.text_area(
        "Enter your diagnostic question or assay challenge:"
    )

    if st.button("Run AI Consultation", type="primary"):
      if not diagnostics_query.strip():
        st.warning("Please enter your question details.")
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
          with st.spinner("Synthesizing diagnostic insights..."):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert molecular diagnostics and microbiology consultant. 
                            Provide precise, scientific guidance on the following inquiry:
                            {diagnostics_query}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 Expert Consultation Summary")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")
