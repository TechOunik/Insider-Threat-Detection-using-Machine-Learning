# Insider Threat Detection Using Machine Learning & Behavioural Rhythm Analysis

An unsupervised machine learning pipeline for detecting malicious insider threats within enterprise log telemetry using **6-hour temporal block feature vectors** and an **Isolation Forest** estimator.

Tested on the **Carnegie Mellon University (CMU) CERT Synthetic Insider Threat Dataset (Release r4.2)** ($N = 1,000$ users, $P = 70$ ground-truth insiders across 17 months).

---

##  Performance Overview

By resolving **temporal dilution** (partitioning activity into 6-hour shifts rather than daily/monthly averages), the model achieves high detection coverage on acute attack bursts:

* **Maximum Detection Rate (Recall):** **91.43%** ($64/70$ target insiders caught at $\alpha = 0.050$)
* **Optimal Operating Point ($\alpha = 0.020$):** $F_1$-Score = **0.2857**, Recall = **65.71%** ($46/70$ caught), User FPR = **22.15%**
* **Low-Noise Triage Mode ($\alpha = 0.001$):** User FPR = **4.09%**, 10 insiders caught with zero prior rules or labels.

---

## Repository Structure

```text
├── data/
│   ├── raw/r4.2/                     # Raw CMU CERT r4.2 CSV logs (logon, device, file, http)
│   └── ground_truth/                 # Answer key mapping CMU CERT insiders
├── detection_output/
│   ├── user_6hr_matrix.csv           # 707,926 6-hour temporal feature instances
│   ├── detected_6hr_blocks.csv       # High-risk anomalous 6-hour instances
│   ├── evaluation_summary.csv        # Multi-threshold evaluation results
│   └── figures/                      # Confusion matrix & performance curve charts
├── src/
│   ├── 01_data_recon.py              # Population verification & ground-truth parsing
│   ├── 02_feature_engineering.py     # 6-Hour temporal shift feature extractor
│   ├── 03_train_detector.py          # Isolation Forest model training
│   ├── 04_evaluate_performance.py    # Contamination sweep & metric evaluation
│   └── 05_generate_diagrams.py       # Evaluation chart generator
├── DEFENSE_NOTES.md                  # Project defense guide & oral examination notes
├── README.md                         # Project documentation
└── requirements.txt                  # Python dependencies

```
---

## Quickstart & Execution
1. Environment Setup
Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Run Pipeline
Bash
# Step 1: Verify baseline population and ground truth
python3 src/01_data_recon.py

# Step 2: Extract 6-hour temporal block features (707,926 instances)
python3 src/02_feature_engineering.py

# Step 3: Train Isolation Forest model
python3 src/03_train_detector.py

# Step 4: Evaluate performance metrics across contamination levels
python3 src/04_evaluate_performance.py

# Step 5: Render high-resolution figures
python3 src/05_generate_diagrams.py

---

## Requirements
* Python 3.10+

* pandas

* scikit-learn

* matplotlib

* seaborn

* numpy
