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

  st.title("🧼 BiofilmAI Biocontrol — Inhibition Modeling Suite")
  st.write("""
    Model and visualize **biofilm inhibition**, **compound interactions**,  
    and **dose‑response behavior** using experimental or datasets, backed by Gemini AI.
    """)

  # ---------------------------------------------------------
  # SIDEBAR NAVIGATION
  # ---------------------------------------------------------
  st.sidebar.header("Biocontrol Modules")
  module = st.sidebar.radio(
      "Select a module:",
      [
          "Inhibition Dataset Explorer",
          "Compound Interaction Modeling",
          "Dose‑Response Visualization",
          "Inhibition Prediction Preview",
          "🤖 Gemini Biocontrol AI Advisor",
      ],
  )

  # ---------------------------------------------------------
  # MODULE 1 — Inhibition Dataset Explorer
  # ---------------------------------------------------------
  if module == "Inhibition Dataset Explorer":
    st.subheader("📊 Inhibition Dataset Explorer")

    uploaded = st.file_uploader("Upload inhibition dataset (CSV)", type=["csv"])

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

      if numeric_cols:
        st.write("### Inhibition Metric Distributions")
        fig, ax = plt.subplots(figsize=(10, 6))
        df[numeric_cols].plot(kind="box", ax=ax)
        ax.set_title("Biofilm Inhibition Metrics")
        st.pyplot(fig)

  # ---------------------------------------------------------
  # MODULE 2 — Compound Interaction Modeling
  # ---------------------------------------------------------
  elif module == "Compound Interaction Modeling":
    st.subheader("🧪 Compound Interaction Modeling")

    st.write("""
        Upload compound inhibition data to model interactions  
        between antimicrobial agents, surfaces, or environmental conditions.
        """)

    uploaded = st.file_uploader(
        "Upload compound interaction dataset (CSV)", type=["csv"]
    )

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      if "compound" in df.columns and "inhibition" in df.columns:
        st.write("### Compound Inhibition Scores")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x="compound", y="inhibition", ax=ax)
        ax.set_title("Compound Inhibition Strength")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
      else:
        st.warning("Required columns not found: compound, inhibition")

  # ---------------------------------------------------------
  # MODULE 3 — Dose‑Response Visualization
  # ---------------------------------------------------------
  elif module == "Dose‑Response Visualization":
    st.subheader("📉 Dose‑Response Visualization")

    uploaded = st.file_uploader(
        "Upload dose‑response dataset (CSV)", type=["csv"]
    )

    if uploaded:
      df = pd.read_csv(uploaded)
      st.write("### Dataset Preview")
      st.dataframe(df.head())

      if "dose" in df.columns and "response" in df.columns:
        st.write("### Dose‑Response Curve")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x="dose", y="response", marker="o", ax=ax)
        ax.set_title("Dose‑Response Curve")
        st.pyplot(fig)
      else:
        st.warning("Required columns not found: dose, response")

  # ---------------------------------------------------------
  # MODULE 4 — Inhibition Prediction Preview
  # ---------------------------------------------------------
  elif module == "Inhibition Prediction Preview":
    st.subheader("🧠 Inhibition Prediction Preview")

    st.write("""
        Enter compound or surface characteristics to preview  
        potential biofilm inhibition behavior.
        """)

    compound = st.text_input("Compound or surface name:")
    concentration = st.number_input(
        "Concentration (µg/mL)", min_value=0.0, value=10.0
    )
    exposure_time = st.number_input(
        "Exposure time (hours)", min_value=0.0, value=24.0
    )

    if st.button("Generate Inhibition Prediction"):
      if compound.strip() == "":
        st.warning("Please enter a compound or surface name.")
      else:
        predicted_inhibition = np.log1p(concentration) * (exposure_time / 24)

        st.write("### Predicted Inhibition Score")
        st.success(f"{predicted_inhibition:.2f}")

        st.write("""
                **Interpretation:**  
                - Higher concentrations increase predicted inhibition  
                - Longer exposure times increase predicted inhibition  
                - This preview is a simplified model for demonstration  
                """)

  # ---------------------------------------------------------
  # MODULE 5 — Gemini Biocontrol AI Advisor (New API Integration)
  # ---------------------------------------------------------
  elif module == "🤖 Gemini Biocontrol AI Advisor":
    st.subheader("🤖 Gemini Biocontrol & Antimicrobial Advisor")
    st.write(
        "Consult the AI advisor for expert evaluation on anti-biofilm compound"
        " efficacy, MIC/MBC interpretation, and microbial resistance trends."
    )

    biocontrol_query = st.text_area(
        "Describe your biocontrol findings, compound parameters, or"
        " experimental questions:"
    )

    if st.button("Run AI Biocontrol Evaluation", type="primary"):
      if not biocontrol_query.strip():
        st.warning("Please enter your query details.")
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
          with st.spinner(
              "Analyzing biofilm inhibition and antimicrobial efficacy..."
          ):
            try:
              genai.configure(api_key=api_key)
              model = genai.GenerativeModel("gemini-1.5-flash")
              prompt = f"""
                            You are an expert microbiologist specializing in biofilm physiology, antimicrobial resistance, and biocontrol strategies. 
                            Provide rigorous, professional feedback and actionable recommendations on the following data/query:
                            {biocontrol_query}
                            """
              response = model.generate_content(prompt)
              st.markdown("### 📋 AI Expert Recommendation")
              st.success(response.text)
            except Exception as e:
              st.error(f"API Error: {e}")
