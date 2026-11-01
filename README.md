# 🧬 SciProAI Platform — BiofilmAI & Clinical Diagnostics Suite

Enterprise commercial and scientific research platform built for molecular diagnostics, laboratory operations, and biofilm research. Designed as a modular Streamlit application leveraging deterministic Python automation (CLSI EP17, EP05, EP09, Westgard rules) and embedded Gemini AI intelligence.

**Live Application:** [SciProAI Platform Live App](https://sciproai-platform-ghrud8jxztkaccryjzx8eh.streamlit.app/)

---

## 🤖 Agentic AI Architecture & RAG Engine

* **`agent_assistant.py` (Supervisor AI Agent & Multi-Tool Router):** Autonomous AI supervisor that inspects user queries across platform domains, routes intent to specialized RAG engines, and synthesizes unified compliance reports.
* **`rag_engine.py` (Shared Grounded RAG Engine):** Platform-wide Retrieval-Augmented Generation module handling PDF/CSV text extraction, context chunking, keyword scoring, and Gemini Flash response grounding across all lab modules.

---

## 🏢 Platform Suite Organization (3 Core Navigation Suites)

### 🏠 Suite 1: Home & Agent Assistant
* **`home.py` (Platform Overview & Global Search):** Central interactive landing page featuring active suite metrics, architectural diagrams, and a grounded platform-wide RAG search engine.
* **`agent_assistant.py` (Autonomous Lab Supervisor):** Interactive agent assistant routing complex cross-module queries.

### 🏢 Suite 2: Enterprise Compliance & Quality Suite
* **`qcai.py` (QA/QC Log & Audit Checker):** Audits instrument maintenance logs, environmental monitoring data, and batch release records against multi-rule Westgard control limits.
* **`sopai.py` (SOP Version Control & Auditor):** Manages standard operating procedure documentation, tracks version changes, and audits procedural compliance against CLSI/ISO standards.
* **`methodai.py` (Method Performance & Assay Verification Suite):** Formats raw instrument outputs, calculates quantitative linearity & amplification efficiency, computes CLSI EP17 detection limits (LoB, LoD, LoQ), parses digital PCR (ddPCR) droplets, and executes method verification/comparison audits.

### 🔬 Suite 3: Bio-Digital Research & Computational Suite
* **`assayai_design.py` (Molecular Assay Design Workspace):** Prototyping qPCR/ddPCR primers, melting temperature (\\(T_m\\)) scoring, probe design, PCR copy number calculation, and dynamic performance visualization.
* **`biofilmai_multimodal.py` (Multimodal Biofilm & AMR Engine):** Integrates spatial FISH fluorescence signals, transcriptomic gene operon expression (log2FC), EPS matrix solute diffusion physics (\\(D_{\text{eff}}/D_0\\)), and AMR genotype-to-phenotype MIC predictions.
* **`biofilmnn_diagnostics.py` (Neural Biofilm Diagnostics):** Microscopic image processing for CLSM/SEM Z-stacks, surface roughness (\\(R_a\\)) computation, biomass volume quantification, and deep-learning viability classification.
* **`dashboards_visualization.py` (Analytics & Trend Dashboards):** Commercial analytics suite tracking polymicrobial co-culture dynamics, multi-site Levey-Jennings QC runs, and matrix penetration heatmaps.
* **`biocontrol_inhibition.py` (Biocontrol & AST Suite):** Broth microdilution MIC/MBC calculations, disk diffusion zone of inhibition profiling against CLSI cutoffs, and Fractional Inhibitory Concentration (FIC) synergy indexing.

---

## 🚀 Project Directory Structure

```text
SciProAI-Platform/
├── app.py                      # Main Streamlit router & navigation controller
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies (streamlit, pandas, numpy, scipy, matplotlib, PyPDF2, google-generativeai)
└── modules/
    ├── home.py                 # Platform Overview & Global RAG Search
    ├── agent_assistant.py      # Supervisor Agent & Multi-Tool RAG Router
    ├── rag_engine.py           # Shared Grounded RAG Engine (PDF/CSV Parsing & Context Retrieval)
    ├── qcai.py                 # Compliance Suite: QA/QC Auditing
    ├── sopai.py                # Compliance Suite: SOP Version Control & Audit
    ├── methodai.py             # Compliance Suite: Method Validation & CLSI EP17/EP05/EP09
    ├── assayai_design.py       # Research Suite: Molecular Assay & Primer Design
    ├── biofilmai_multimodal.py # Research Suite: Spatial FISH & AMR Omics Engine
    ├── biofilmnn_diagnostics.py# Research Suite: Microscopic Image & Neural Viability
    ├── dashboards_visualization.py # Research Suite: Multi-Site & Polymicrobial Dashboards
    └── biocontrol_inhibition.py # Research Suite: MIC/MBC & Combination FIC Synergy
