import os
import google.generativeai as genai
import streamlit as st


def main():
  st.subheader("🤖 Gemini Supervisor Agent")
  st.write(
      "The supervisor agent analyzes your request and coordinates across"
      " AssayAI, BiofilmAI, Compliance, and Biocontrol."
  )

  user_query = st.text_input(
      "Enter a multi-domain research or compliance query:"
  )

  if user_query:
    if not os.environ.get("GEMINI_API_KEY"):
      st.error(
          "⚠️ GEMINI_API_KEY is missing. Please check your Streamlit Secrets."
      )
      return

    with st.spinner("🤖 Supervisor Agent analyzing and routing query..."):
      try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
                You are the SciProAI Supervisor Agent. 
                User Query: {user_query}
                Provide a structured scientific and compliance response, identifying which suite/module should handle this data.
                """
        response = model.generate_content(prompt)

        st.success("Analysis Complete!")
        st.markdown("### Supervisor Output")
        st.write(response.text)

      except Exception as e:
        st.error(f"Error communicating with Gemini API: {e}")
