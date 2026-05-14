# Insider Threat Detection using Machine Learning

## Project Overview
This research focuses on identifying insider threats by **analysing behavioural** patterns within an **organisational** environment. By **utilising** the **CERT r4.2** dataset, the system seeks to detect "rhythm breaks" in user activity using **unsupervised learning** techniques.

## Technical Specification
- **Operating System:** Ubuntu 24.04 (Host)
- **Programming Language:** Python 3.12
- **Key Libraries:** Pandas, Scikit-learn, Matplotlib
- **Dataset:** CERT Insider Threat Test Dataset r4.2 (32 million events)

## Methodology
- **Data Ingestion:** Efficiently **handling** 16GB of raw telemetry (HTTP, Logon, Device, and Email logs).
- **Feature Engineering:** **Organising** activity into 6-hour temporal windows for **behavioural profiling**.
- **Modelling:** Implementation of **Isolation Forest** to identify outliers and anomalies.

## Project Log
- **[12th May, 2026]:** I Successfully **initialised** repository and **established** local ingestion pipeline for the **14GB HTTP log** files.
- **[13th May 2026]:** I established a lightweight data ingestion pipeline using **Python** and **Pandas**. Opted for a chunked-processing approach to handle the 16GB dataset efficiently on local hardware, ensuring a minimal storage footprint and avoiding the overhead of heavy SIEM indexing.
