import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, filters, morphology, measure, segmentation
from scipy import ndimage as ndi

def main():
    # ---------------------------------------------------------
    # PAGE CONFIGURATION
    # ---------------------------------------------------------
    st.set_page_config(
        page_title="BiofilmAI — Multimodal Biofilm Modeling Suite",
        layout="wide"
    )

    st.title("🔬 BiofilmAI — Multimodal Biofilm Modeling Suite")
    st.write("""
    This suite integrates **gene expression analysis**, **microscopy image processing**,  
    **multimodal fusion**, and **research document summarization** into a unified scientific workflow.
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
            "Research Document Summary"
        ]
    )

    # ---------------------------------------------------------
    # MODULE 1 — Gene Expression Checker
    # ---------------------------------------------------------
    if module == "Gene Expression Checker":
        st.subheader("🧬 Gene Expression Checker")

        uploaded = st.file_uploader("Upload differential expression CSV", type=["csv", "tsv"])

        if uploaded:
            df = pd.read_csv(uploaded)
            st.write("### Preview")
            st.dataframe(df.head())

            # Volcano plot
            if "log_FC" in df.columns and "deseq.p-value" in df.columns:
                st.write("### Volcano Plot")

                fig, ax = plt.subplots(figsize=(8,6))
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
    if module == "Biofilm Image Analyzer":
        st.subheader("🧫 Biofilm Image Analyzer")

        uploaded_img = st.file_uploader("Upload microscopy image", type=["png", "jpg", "jpeg"])

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
            fig, ax = plt.subplots(figsize=(8,6))
            ax.imshow(labels, cmap="nipy_spectral")
            ax.set_title("Watershed Segmentation")
            ax.axis("off")
            st.pyplot(fig)

            st.write("### Object Count:", labels.max())

    # ---------------------------------------------------------
    # MODULE 3 — Multimodal Fusion Hub
    # ---------------------------------------------------------
    if module == "Multimodal Fusion Hub":
        st.subheader("🧪 Multimodal Fusion Hub")

        st.write("""
        Combine **gene expression embeddings** and **image embeddings**  
        to create unified multimodal predictions.
        """)

        expr_file = st.file_uploader("Upload gene expression feature table", type=["csv"])
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
    # MODULE 4 — Research Document Summary
    # ---------------------------------------------------------
    if module == "Research Document Summary":
        st.subheader("📄 Research Document Summary")

        text = st.text_area("Paste scientific text to summarize:")

        if st.button("Summarize"):
            if len(text.strip()) == 0:
                st.warning("Please paste text first.")
            else:
                # Simple placeholder summary
                st.write("### Summary")
                st.write(text[:300] + "...")
