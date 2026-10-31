# 🧬 SciProAI Platform

Enterprise commercial and scientific research platform built for molecular diagnostics, laboratory operations, and biofilm research. Designed as a modular Streamlit application leveraging deterministic Python automation and embedded Gemini AI intelligence.

**Live Application:** [SciProAI Platform Live App](https://sciproai-platform-ghrud8jxztkaccryjzx8eh.streamlit.app/)

---

## 🤖 Agentic AI & RAG Engine

* **`agent_assistant.py` (Supervisor AI Agent & Multi-Tool Router):** Autonomous AI supervisor that inspects user queries across platform domains, routes intent to specialized RAG engines, and synthesizes unified compliance reports.
* **`rag_engine.py` (Shared Grounded RAG Engine):** Platform-wide Retrieval-Augmented Generation module handling PDF/CSV text extraction, context chunking, keyword scoring, and Gemini Flash response grounding across all lab modules.

---

## 🏢 Business Modules

* **`qcai.py` (QA/QC Log & Audit Checker):** Audits instrument maintenance logs, environmental monitoring data, and batch release records against quality control thresholds.
* **`sopai.py` (SOP Version Control & Auditor):** Manages standard operating procedure documentation, tracks version changes, and audits procedural compliance.
* **`methodai.py` (Method Performance, Verification & Assay Data Suite):** Formats raw instrument outputs, calculates quantitative linearity & amplification efficiency, computes CLSI EP17 detection limits (LoB, LoD, LoQ), parses digital PCR (ddPCR) droplets, and executes method verification/comparison audits.

---

## 🔬 Research Modules

* **`assayai_design.py`:** Advanced molecular assay design and primer/probe evaluation suite.
* **`biofilmai_multimodal.py`:** Multimodal biofilm modeling and comparative analysis.
* **`biofilmnn_diagnostics.py`:** Neural network diagnostics for microbial biofilms.
* **`dashboards_visualization.py`:** Interactive data visualization dashboards for complex analytics.
* **`biocontrol_inhibition.py`:** Antimicrobial inhibition and biocontrol analytics.

---

## 🚀 Project Structure

```text
sciproai/
│
├── app.py                      # Main Streamlit router & navigation controller
├── README.md                   # Project documentation
│
├── modules/
│   ├── home.py                 # Central Platform Hub & Interactive Guide
│   ├── agent_assistant.py      # Supervisor Agent & Multi-Tool RAG Router
│   ├── rag_engine.py           # Shared Grounded RAG Engine (PDF/CSV Chunking & Retrieval)
│   ├── qcai.py                 # Business Module 1: QA/QC Auditing
│   ├── sopai.py                # Business Module 2: SOP Compliance
│   ├── methodai.py             # Business Module 3: Method Performance & Assay Data
│   ├── assayai_design.py       # Research Module: Molecular Assay Design
│   ├── biofilmai_multimodal.py # Research Module: Multimodal Biofilm Modeling
│   ├── biofilmnn_diagnostics.py# Research Module: Neural Network Diagnostics
│   ├── dashboards_visualization.py # Research Module: Analytics Dashboards
│   └── biocontrol_inhibition.py # Research Module: Biocontrol Analytics
│
└── requirements.txt            # Dependencies (streamlit, pandas, numpy, scipy, PyPDF2, google-generativeai)
