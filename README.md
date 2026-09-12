# SciProAI Platform



Enterprise commercial and scientific research platform built for molecular diagnostics, laboratory operations, and biofilm research. Designed as a modular Streamlit application leveraging deterministic Python automation.



## 🏢 Core Commercial Business Modules

1. **`qcai.py` (QA/QC Log & Audit Checker):** Audits instrument maintenance logs, environmental monitoring data, and batch release records against quality control thresholds.

2. **`sopai.py` (SOP Version Control & Auditor):** Manages standard operating procedure documentation, tracks version changes, and audits procedural compliance.

3. **`methodai.py` (Method Performance, Verification & Assay Data Suite):** Formats raw instrument outputs, calculates quantitative linearity & amplification efficiency, computes CLSI EP17 detection limits (LoB, LoD, LoQ), parses digital PCR (ddPCR) droplets, and executes method verification/comparison audits.



## 🔬 Scientific Research Suites

* **`assayai_design`:** Advanced molecular assay design and primer/probe evaluation suite.

* **Biofilm & Biocontrol Modules:** Multimodal modeling, neural network diagnostics, interactive visualization dashboards, and antimicrobial inhibition analysis.



## 🚀 Project Structure

```text

sciproai/

│

├── app.py                  # Main Streamlit router & navigation controller

├── home.py                 # Landing page & platform overview dashboard

├── README.md               # Project documentation

│

├── modules/

│   ├── qcai.py             # Business Module 1: QA/QC Auditing

│   ├── sopai.py            # Business Module 2: SOP Compliance

│   ├── methodai.py         # Business Module 3: Method Performance & Assay Data

│   └── ... (Research modules including assayai_design)

│

└── requirements.txt        # Dependencies (streamlit, pandas, numpy, scipy) 

