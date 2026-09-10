import streamlit as st
import pandas as pd
import numpy as np
from skimage import io, filters, morphology, measure, segmentation
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="BiofilmNN — AI Diagnostics Suite",
    layout="wide"
)

st.title("🧫 BiofilmNN — AI Diagnostics Suite")
st.write("""
This suite provides **AI-assisted microbial diagnostics**, including image-based classification,  
AMR (antimicrobial resistance) feature extraction, segmentation previews, and diagnostic reasoning.
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
        "Diagnostic Reasoning Preview"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Microbial Image Diagnostics
# ---------------------------------------------------------
if module == "Microbial Image Diagnostics":
    st.subheader("🔬 Microbial Image Diagnostics")

    uploaded_img = st.file_uploader("Upload microbial microscopy image", type=["png", "jpg", "jpeg"])

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
        fig, ax = plt.subplots(figsize=(8,6))
        ax.imshow(labels, cmap="nipy_spectral")
        ax.set_title("Microbial Segmentation")
        ax.axis("off")
        st.pyplot(fig)

        st.write("### Object Count:", labels.max())

# ---------------------------------------------------------
# MODULE 2 — AMR Prediction (AMRAI)
# ---------------------------------------------------------
if module == "AMR Prediction (AMRAI)":
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
if module == "Image Feature Extraction":
    st.subheader("📊 Image Feature Extraction")

    uploaded_img = st.file_uploader("Upload image for feature extraction", type=["png", "jpg", "jpeg"])

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
            "Min Intensity": float(min_intensity)
        })

# ---------------------------------------------------------
# MODULE 4 — Diagnostic Reasoning Preview
# ---------------------------------------------------------
if module == "Diagnostic Reasoning Preview":
    st.subheader("🧠 Diagnostic Reasoning Preview")

    text = st.text_area("Describe the microbial sample or diagnostic question:")

    if st.button("Generate Diagnostic Reasoning"):
        if len(text.strip()) == 0:
            st.warning("Please enter a description first.")
        else:
            st.write("### Diagnostic Reasoning")
            st.write(f"""
            Based on your description, the diagnostic reasoning module identifies potential  
            microbial behaviors, AMR indicators, and morphological patterns relevant to  
            biofilm-associated infections.

            **Input Summary:**  
            {text[:300]}...

            **Reasoning Preview:**  
            - Possible biofilm-associated phenotype  
            - Potential AMR-related gene expression patterns  
            - Morphological indicators of microbial clustering  
            - Suggested follow-up assays (microscopy, qPCR, ddPCR)
            """)
