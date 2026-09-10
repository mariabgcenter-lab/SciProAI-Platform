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
business.add_page("BizDocAI", "pages/1_6_bizdocai.py")
business.add_page("BizAgentAI", "pages/1_7_bizagentai.py")

research = st.PageGroup("🔬 Research Suite")

research.add_page("BiofilmAI Multimodal", "pages/2_1_biofilmai_multimodal.py")
research.add_page("BiofilmNN Diagnostics", "pages/2_2_biofilmnn_diagnostics.py")
research.add_page("Dashboards Visualization", "pages/2_3_dashboards_visualization.py")
research.add_page("Biocontrol Inhibition", "pages/2_4_biocontrol_inhibition.py")
research.add_page("AssayAI Design", "pages/2_5_assayai_design.py")

# ---------------------------
# RUN THE APP
# ---------------------------

pg = st.navigation([business, research])
pg.run()
