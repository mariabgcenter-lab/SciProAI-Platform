import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="BizAgentAI — Business Automation Agent",
    layout="wide"
)

st.title("🤖 BizAgentAI — Business Automation Agent")
st.write("""
Automate **business workflows**, generate structured documentation,  
and run multi-step reasoning tasks for laboratory and scientific operations.
""")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.header("BizAgentAI Modules")
module = st.sidebar.radio(
    "Select a module:",
    [
        "Workflow Automation",
        "Document Generator",
        "Business Reasoning Engine"
    ]
)

# ---------------------------------------------------------
# MODULE 1 — Workflow Automation
# ---------------------------------------------------------
if module == "Workflow Automation":
    st.subheader("🔁 Workflow Automation")

    st.write("Define a multi-step business workflow to automate.")

    workflow_name = st.text_input("Workflow Name:")
    num_steps = st.number_input("Number of steps", min_value=1, max_value=50, value=5)

    steps = []
    for i in range(int(num_steps)):
        step = st.text_input(f"Step {i+1}:", key=f"wf_step_{i}")
        steps.append(step)

    if st.button("Generate Workflow Automation Summary"):
        if not workflow_name.strip():
            st.warning("Please enter a workflow name.")
        else:
            st.markdown("### Workflow Automation Summary")
            st.write(f"**Workflow Name:** {workflow_name}")
            st.write("### Steps")
            for i, s in enumerate(steps, start=1):
                if s.strip():
                    st.write(f"- Step {i}: {s}")

# ---------------------------------------------------------
# MODULE 2 — Document Generator
# ---------------------------------------------------------
if module == "Document Generator":
    st.subheader("📄 Document Generator")

    doc_type = st.selectbox(
        "Document Type:",
        ["SOP", "Validation Plan", "QC Record", "Training Record", "Business Summary"]
    )

    title = st.text_input("Document Title:")
    content = st.text_area("Key Content / Notes:")

    if st.button("Generate Document"):
        if not title.strip():
            st.warning("Please enter a document title.")
        else:
            st.markdown("### Generated Document")
            st.write(f"**Type:** {doc_type}")
            st.write(f"**Title:** {title}")
            st.write(f"**Content:**\n{content}")

# ---------------------------------------------------------
# MODULE 3 — Business Reasoning Engine
# ---------------------------------------------------------
if module == "Business Reasoning Engine":
    st.subheader("🧠 Business Reasoning Engine")

    st.write("Paste business logic, workflow reasoning, or decision-making text.")

    reasoning_text = st.text_area("Business reasoning input:")

    if st.button("Evaluate Reasoning"):
        if not reasoning_text.strip():
            st.warning("Please paste reasoning text.")
        else:
            st.write("### Reasoning Evaluation (Illustrative)")
            st.write("""
            - Structure appears coherent  
            - Reasoning follows logical progression  
            - No major contradictions detected  
            - Recommend human review for final approval  
            """)
