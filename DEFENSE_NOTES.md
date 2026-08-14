# DEFENSE_NOTES.md — Final Year Project Defense Guide
**Candidate:** Obioma Felicity Uzoh  
**Topic:** Development of an Insider Threat Detection System Using Machine Learning and Behavioural Rhythm Analysis  
**Dataset:** CMU CERT Insider Threat Dataset (Release r4.2)  
**Theoretical Anchor:** Routine Activity Theory (RAT) — Cohen & Felson (1979)  

---

## 1. Core Methodological Position (The "Elevator Pitch")

1. **Perimeter Defense is Bypassed:** Over 78% of modern security breaches involve valid internal credentials. Perimeter firewalls cannot stop an authenticated user executing actions within the network.
2. **Behavior-Driven, Not Identity-Driven:** Evaluates observable behavioral shifts across time windows rather than assuming a specific user ID is inherently malicious.
3. **Metadata over Content:** Analyzes interaction metadata (timestamps, USB connect counts, transaction frequencies) rather than reading private email or file contents, balancing monitoring with privacy.
4. **Lightweight ML over Black-Box Deep Learning:** Unsupervised Isolation Forest trained on engineered 6-hour temporal vectors executes in under 15 seconds on dual-core hardware, providing explainable decisions without expensive GPU infrastructure.

---

## 2. Empirical Ground Truth & Dataset Reality

* **Total Corporate Population ($N$):** $1,000$ unique simulated employees tracked across 17 months.
* **Verified CERT r4.2 Malicious Insiders ($P$):** Exactly $70$ unique target threat actors.
* **Verified Benign Employees ($N_{\text{benign}}$):** Exactly $930$ benign users.
* **Evaluated Feature Space:** **707,926 total 6-hour temporal block instances** across four multi-vector streams:
  * `logon.csv` $\rightarrow$ Session authentication counts per 6-hour shift.
  * `device.csv` $\rightarrow$ External removable USB insertion events.
  * `file.csv` $\rightarrow$ Document access and file harvesting volume.
  * `http.csv` $\rightarrow$ Web hits targeting exfiltration portals (Dropbox, WikiLeaks, Mega), job sites (Monster, Indeed), or keylogger downloads.

---

## 3. Verified Empirical Results (6-Hour Temporal Block Matrix)

| Contamination ($\alpha$) | TP | FP | FN | TN | Precision (%) | Recall (%) | $F_1$-Score | User FPR (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.001** | 10 | 38 | 60 | 892 | **20.83%** | 14.29% | 0.1695 | **4.09%** |
| **0.005** | 24 | 93 | 46 | 837 | 20.51% | 34.29% | 0.2567 | 10.00% |
| **0.010** | 32 | 132 | 38 | 798 | 19.51% | 45.71% | 0.2735 | 14.19% |
| **0.020** | **46** | **206** | **24** | **724** | **18.25%** | **65.71%** | **0.2857** | **22.15%** |
| **0.030** | 58 | 342 | 12 | 588 | 14.50% | 82.86% | 0.2468 | 36.77% |
| **0.050** | **64** | **428** | **6** | **502** | **13.01%** | **91.43%** | **0.2278** | **46.02%** |

### Key Experimental Insights:
1. **Resolution of Temporal Dilution:** Moving from macro-level user profiling to 6-hour temporal blocks boosted maximum threat actor detection (Recall) from **$27.14\%$ to $91.43\%$** (isolating $64$ of the $70$ target insiders).
2. **Optimal Balance Point ($\alpha = 0.020$):** $F_1$-score peaks at **$0.2857$**, catching **46 malicious insiders** ($65.71\%$ Recall) while flagging an average of only 12 benign users per month.

---

## 4. Key Academic Answers for Panel Defense Questions

### Q1: "Why did you use 6-hour temporal blocks instead of daily or overall averages?"
* **Answer:** Malicious insider actions occur in short, intense bursts (e.g., a 2-hour USB file copy at 2:00 AM). Averaging over months or full days dilutes that short spike into standard routine. Partitioning the day into four 6-hour blocks (00:00–06:00, 06:00–12:00, 12:00–18:00, 18:00–24:00) isolates the exact shift where the anomaly occurred, increasing Recall from $27.14\%$ to $91.43\%$.

### Q2: "Your model has false positives. Is that a system failure?"
* **Answer:** No. Unsupervised anomaly detection measures **statistical variance, not human intent**. A benign employee pulling an all-nighter or copying large files for an urgent migration looks mathematically identical to an exfiltrating insider. In an enterprise SOC, our unsupervised model acts as a **tier-1 triage filter**, filtering **707,926 raw log blocks** down to high-risk instances for human analyst review.

### Q3: "Why choose Isolation Forest over Deep Learning (LSTM/Autoencoders)?"
* **Answer:** Isolation Forest isolates anomalies explicitly using tree partitioning rather than profiling normal points. Deep Learning models require GPUs, heavy computation, and act as "black boxes" that cannot explain decisions. Isolation Forest executes in under 15 seconds on standard dual-core laptop hardware while offering clear feature path explainability for security auditors.

### Q4: "How does your system implement Routine Activity Theory (RAT)?"
* **Answer:** Criminological RAT states crime occurs when a Motivated Offender, Suitable Target, and Absence of a Capable Guardian converge. In our system:
  * **Offender:** The authenticated insider holding valid access credentials.
  * **Target:** Sensitive corporate IP / file systems.
  * **Capable Guardian:** Our Isolation Forest model monitoring 6-hour temporal shifts, detecting the behavioral disruption before data exfiltration is complete.
