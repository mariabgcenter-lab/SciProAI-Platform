import os
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


def main():
  # ---------------------------------------------------------
  # PAGE CONFIGURATION (Handled globally by app.py)
  # ---------------------------------------------------------

  st.title("📊 BiofilmAI Dashboards — Visualization Suite")
  st.write("""
    Interactive dashboards for exploring **biofilm behavior**, **gene expression patterns**,  
    **microbiome metrics**, and **multimodal fusion datasets**, backed by Gemini AI.
    """)

  # ---------------------------------------------------------
  # SIDEBAR NAVIGATION
  # ---------------------------------------------------------
  st.sidebar.header("Dashboard Modules")
  module = st.sidebar.radio(
      "Select a dashboard:",
      [
          "Gene Expression Dashboard",
          "Biofilm Behavior Dashboard",
          "MicrobiomeAI Dashboard",
          "Image Metrics Dashboard",
          "Fusion Data Dashboard",
          "🤖 Gemini Dashboard AI Advisor",
      ],
  )

  # ---------------------------------------------------------
  # MODULE 1 — Gene Expression Dashboard
  # ---------------------------------------------------------
  if module == "Gene Expression Dashboard":
    st.subheader("🧬 Gene Expression Dashboard")

    uploaded = st.file_uploader("Upload gene expression CSV", type=["csv"])

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      # Distribution plot
      if "log_FC" in df.columns:
        st.write("### log2 Fold Change Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df["log_FC"], kde=True, ax=ax)
        ax.set_title("log2 Fold Change Distribution")
        st.pyplot(fig)

      # Volcano plot
      if "log_FC" in df.columns and "deseq.p-value" in df.columns:
        st.write("### Volcano Plot")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df["log_FC"], -np.log10(df["deseq.p-value"]), s=10, alpha=0.6)
        ax.set_xlabel("log2 Fold Change")
        ax.set_ylabel("-log10(p-value)")
        ax.set_title("Volcano Plot")
        st.pyplot(fig)

  # ---------------------------------------------------------
  # MODULE 2 — Biofilm Behavior Dashboard
  # ---------------------------------------------------------
  elif module == "Biofilm Behavior Dashboard":
    st.subheader("🧫 Biofilm Behavior Dashboard")

    uploaded = st.file_uploader(
        "Upload biofilm behavior dataset (CSV)", type=["csv"]
    )

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

      if numeric_cols:
        st.write("### Behavior Metric Distributions")
        fig, ax = plt.subplots(figsize=(10, 6))
        df[numeric_cols].plot(kind="box", ax=ax)
        ax.set_title("Biofilm Behavior Metrics")
        st.pyplot(fig)

  # ---------------------------------------------------------
  # MODULE 3 — MicrobiomeAI Dashboard
  # ---------------------------------------------------------
  elif module == "MicrobiomeAI Dashboard":
    st.subheader("🧪 MicrobiomeAI Dashboard")

    uploaded = st.file_uploader("Upload microbiome dataset (CSV)", type=["csv"])

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      # Abundance heatmap
      st.write("### Microbial Abundance Heatmap")
      fig, ax = plt.subplots(figsize=(10, 6))
      sns.heatmap(df.set_index(df.columns[0]), cmap="viridis", ax=ax)
      st.pyplot(fig)

  # ---------------------------------------------------------
  # MODULE 4 — Image Metrics Dashboard
  # ---------------------------------------------------------
  elif module == "Image Metrics Dashboard":
    st.subheader("📸 Image Metrics Dashboard")

    uploaded = st.file_uploader("Upload image metrics CSV", type=["csv"])

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

      if numeric_cols:
        st.write("### Metric Correlation Matrix")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax
        )
        st.pyplot(fig)

  # ---------------------------------------------------------
  # MODULE 5 — Fusion Data Dashboard
  # ---------------------------------------------------------
  elif module == "Fusion Data Dashboard":
    st.subheader("🔗 Fusion Data Dashboard")

    expr_file = st.file_uploader("Upload gene expression features", type=["csv"])
    img_file = st.file_uploader("Upload image features", type=["csv"])

    if expr_file and img_file:
      expr = pd.read_csv(expr_file)
      img = pd.read_csv(img_file)

      st.write("### Gene Expression Features")
      st.dataframe(expr.head())

      st.write("### Image Features")
      st.dataframe(img.head())

      # Fusion preview
      st.write("### Early Fusion Preview")
      fused = pd.concat([expr, img], axis=1)
      st.dataframe(fused.head())

      # Correlation heatmap
      st.write("### Fusion Correlation Matrix")
      fig, ax = plt.subplots(figsize=(10, 6))
      sns.heatmap(fused.corr(), cmap="coolwarm", ax=ax)
      st.pyplot(fig)

  # ---------------------------------------------------------
  # MODULE 6 — Gemini Dashboard AI Advisor
  # ---------------------------------------------------------
  elif module == "🤖 Gemini Dashboard AI Advisor":
    st.subheader("🤖 Dashboard & Multi-Omics Analytics Advisor")
    st.write(
        "Consult the AI advisor to interpret complex dashboard trends,"
        " correlation matrices, and multi-omics fusion patterns."
    )

    dashboard_query = st.text_area(
        "Describe your dashboard observations, anomalous clusters, or"
        " analytical questions:"
    )

    if st.button("Run AI Dashboard Analysis", type="primary"):
      if not dashboard_query.strip():
        st.warning("Please enter your analysis details.")
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
          with st.spinner("Synthesizing dashboard analytics..."):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert computational biologist and data scientist specializing in multi-omics visualization and biofilm analytics. 
                            Provide rigorous, professional interpretation and actionable insights based on the following dashboard observation:
                            {dashboard_query}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 AI Analytics Expert Insight")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")
