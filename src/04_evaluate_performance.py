import os, glob
import pandas as pd
from sklearn.ensemble import IsolationForest

def evaluate():
    print("=== [STEP 4] EVALUATING PERFORMANCE & CONFUSION METRICS ===")
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
    matrix = pd.read_csv("detection_output/user_day_matrix.csv")
    feature_cols = ['off_hours_logons', 'usb_connects', 'exfil_hits', 'file_actions']
    X = matrix[feature_cols].values

    results = []
    for alpha in [0.001, 0.005, 0.010, 0.020, 0.030, 0.050]:
        model = IsolationForest(n_estimators=100, contamination=alpha, random_state=42)
        preds = model.fit_predict(X)
        flagged = set(matrix[preds == -1]['user'].astype(str).unique())

        TP = len(flagged.intersection(gt_users))
        FP = len(flagged - gt_users)
        FN = len(gt_users - flagged)
        TN = len(pop_users) - len(flagged | gt_users)

        prec = TP / (TP + FP) if (TP + FP) > 0 else 0
        rec = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0
        fpr = FP / (FP + TN) if (FP + TN) > 0 else 0

        results.append({
            'Contamination': alpha, 'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN,
            'Precision': f"{prec*100:.2f}%", 'Recall': f"{rec*100:.2f}%",
            'F1-Score': f"{f1:.4f}", 'FPR': f"{fpr*100:.2f}%"
        })

    res_df = pd.DataFrame(results)
    res_df.to_csv("detection_output/evaluation_summary.csv", index=False)
    print(res_df.to_string(index=False))
    print("\n✅ Final Evaluation Table Saved to detection_output/evaluation_summary.csv")

if __name__ == "__main__":
    evaluate()
