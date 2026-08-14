import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

def generate_visuals():
    print("=== [STEP 5] GENERATING REAL 6-HOUR TEMPORAL BLOCK DIAGRAMS ===")
    os.makedirs("detection_output/figures", exist_ok=True)
    
    # Set academic plotting style
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})

    # 1. Load Data & Perform Evaluation at Optimal Threshold (alpha = 0.020)
    data_dir = "data/raw/r4.2"
    logon_df = pd.read_csv(f"{data_dir}/logon.csv", usecols=['user'])
    pop_users = set(logon_df['user'].dropna().astype(str).unique())

    gt_files = glob.glob("answers/**/*.csv", recursive=True) + glob.glob("data/ground_truth/**/*.csv", recursive=True)
    raw_gt = set()
    for f in gt_files:
        basename = os.path.basename(f)
        if "insiders.csv" in basename:
            try:
                df = pd.read_csv(f)
                cols = [c for c in df.columns if 'user' in c.lower() or 'insider' in c.lower()]
                if cols: raw_gt.update(df[cols[0]].dropna().astype(str).unique())
            except Exception: pass
        parts = basename.replace('.csv', '').split('-')
        if len(parts) >= 3 and "r4.2" in basename: raw_gt.add(parts[-1])
            
    gt_users = raw_gt.intersection(pop_users)
    matrix = pd.read_csv("detection_output/user_6hr_matrix.csv")
    feature_cols = ['logon_count', 'usb_connects', 'exfil_hits', 'file_actions']
    X = matrix[feature_cols].values

    # Fit Model at Optimal Contamination (alpha = 0.020)
    optimal_alpha = 0.020
    model = IsolationForest(n_estimators=100, contamination=optimal_alpha, random_state=42)
    preds = model.fit_predict(X)
    flagged = set(matrix[preds == -1]['user'].astype(str).unique())

    TP = len(flagged.intersection(gt_users))
    FP = len(flagged - gt_users)
    FN = len(gt_users - flagged)
    TN = len(pop_users) - len(flagged | gt_users)

    # -------------------------------------------------------------
    # DIAGRAM 1: CONFUSION MATRIX HEATMAP (6-HOUR BLOCK RUN)
    # -------------------------------------------------------------
    print("-> Generating Real Confusion Matrix Heatmap...")
    cm_data = np.array([[TN, FP], [FN, TP]])
    plt.figure(figsize=(7, 5.5))
    
    sns.heatmap(cm_data, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Predicted Benign', 'Predicted Malicious'],
                yticklabels=['Actual Benign', 'Actual Malicious'],
                annot_kws={"size": 14, "weight": "bold"})
    
    plt.title(f'Isolation Forest Confusion Matrix (α = {optimal_alpha})', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Ground Truth Class', fontsize=12, fontweight='bold')
    plt.xlabel('Model Prediction', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig("detection_output/figures/confusion_matrix.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # DIAGRAM 2: CONTAMINATION TRADE-OFF CURVE (6-HOUR BLOCK RUN)
    # -------------------------------------------------------------
    print("-> Generating Real Precision-Recall-FPR Sweep Curve...")
    alphas = [0.001, 0.005, 0.010, 0.020, 0.030, 0.050]
    precisions, recalls, f1s, fprs = [], [], [], []

    for a in alphas:
        m = IsolationForest(n_estimators=100, contamination=a, random_state=42)
        p = m.fit_predict(X)
        flg = set(matrix[p == -1]['user'].astype(str).unique())
        
        tp_i = len(flg.intersection(gt_users))
        fp_i = len(flg - gt_users)
        fn_i = len(gt_users - flg)
        tn_i = len(pop_users) - len(flg | gt_users)

        prec_i = tp_i / (tp_i + fp_i) if (tp_i + fp_i) > 0 else 0
        rec_i = tp_i / (tp_i + fn_i) if (tp_i + fn_i) > 0 else 0
        f1_i = (2 * prec_i * rec_i) / (prec_i + rec_i) if (prec_i + rec_i) > 0 else 0
        fpr_i = fp_i / (fp_i + tn_i) if (fp_i + tn_i) > 0 else 0

        precisions.append(prec_i * 100)
        recalls.append(rec_i * 100)
        f1s.append(f1_i)
        fprs.append(fpr_i * 100)

    plt.figure(figsize=(8, 5))
    plt.plot(alphas, recalls, marker='o', linewidth=2.5, color='#d95f02', label='Recall (%)')
    plt.plot(alphas, precisions, marker='s', linewidth=2.5, color='#7570b3', label='Precision (%)')
    plt.plot(alphas, fprs, marker='^', linewidth=2, linestyle='--', color='#e7298a', label='False Positive Rate (%)')

    plt.axvline(x=0.020, color='gray', linestyle=':', label='Optimal Operating Threshold (α = 0.020)')
    plt.title('Detection Performance Across 6-Hour Temporal Block Contamination Levels', fontsize=12, fontweight='bold')
    plt.xlabel('Contamination Rate (α)', fontsize=11, fontweight='bold')
    plt.ylabel('Percentage (%)', fontsize=11, fontweight='bold')
    plt.legend(loc='center right', frameon=True)
    plt.tight_layout()
    plt.savefig("detection_output/figures/contamination_tradeoff_curve.png", dpi=300)
    plt.close()

    print("\n✅ REAL 6-Hour Block Diagrams Saved to detection_output/figures/:")
    print("   1. detection_output/figures/confusion_matrix.png")
    print("   2. detection_output/figures/contamination_tradeoff_curve.png\n")

if __name__ == "__main__":
    generate_visuals()
