# SciProAI Platform — Commercial Laboratory Automation & Research Suite

Live Interactive App:  
https://bg-biowrite-scientific.streamlit.app/

The SciProAI Platform is a specialized Streamlit application designed to bridge advanced scientific research with deterministic, regulatory-aligned software tools for private-sector commercial testing and diagnostic laboratories.

SciProAI integrates 8 focused suites across scientific research and core laboratory operations, providing a robust environment for analytical data formatting, QA/QC log auditing, SOP compliance, and multimodal biofilm modeling.

---

# 🧬 Platform Architecture

SciProAI Platform is organized into two primary sections:

---

## 🔬 Research AI Suites (5)

Advanced scientific tools for modeling, diagnostics, visualization, biocontrol, and assay design.

### 1. BiofilmAI — Multimodal Biofilm Modeling Suite
- Gene expression analysis  
- Microscopy image processing  
- Multimodal fusion  
- Research document summarization  

### 2. BiofilmNN — AI Diagnostics Suite
- Microbial imaging diagnostics  
- AMR prediction (AMRAI Module)  
- Diagnostic workflows  

### 3. BiofilmAI Dashboards — Interactive Visualization Suite
- MicrobiomeAI visualization  
- Biofilm behavior dashboards  
- Fusion data exploration  

### 4. BiofilmAI Biocontrol — Inhibition Modeling Suite
- Biofilm inhibition prediction  
- Compound/surface interaction modeling  
- Biocontrol strategy evaluation  

### 5. AssayAI — Molecular Assay Design Suite
- ddPCR/qPCR optimization  
- PCRoptAI — Assay Module  
- Assay modeling and comparison  

---

## 🏢 Commercial Laboratory Micro-Tools (3)

High-value, deterministic operational tools built to solve painful administrative, validation, and compliance bottlenecks for private commercial labs.

### 1. QA/QC Log & Audit Checker (`qcai`)
- Upload daily instrument or QC logs to instantly flag outliers, missing parameters, or non-conformance trends before internal audits.

### 2. Assay Data Formatter & Validator (`validateai`)
- Clean raw export files from PCR, qPCR, or ddPCR instruments, calculate baseline metrics (such as standard curve parameters), and format into compliance-ready reports.

### 3. SOP Version Control & Auditor (`sopai`)
- Audit and cross-reference Standard Operating Procedures against updated ISO or environmental standards to identify out-of-date documentation.

---

# 📁 Folder Structure (Modules‑Only Architecture)

All application modules live inside the `modules/` directory.  
The `pages/` folder is not used, ensuring a clean layout with sidebar‑only navigation and no auto‑generated Streamlit menu.
