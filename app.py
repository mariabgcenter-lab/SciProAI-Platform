import streamlit as st

st.set_page_config(
    page_title="BG BioWrite Scientific",
    page_icon="🧬",
    layout="wide"
)

# ---------------------------
# PAGE GROUPS
# ---------------------------

business = st.PageGroup("🏢 Business Suite")

business.add_page("SOPAI", "pages/1_1_sopai.py")
business.add_page("ValidateAI", "pages/1_2_validateai.py")
business.add_page("QCAI", "pages/1_3_qcai.py")
business.add_page("TrainAI", "pages/1_4_trainai.py")
business.add_page("ReasonAI", "pages/1_5_reasonai.py")
business.add_page("BizDoc
