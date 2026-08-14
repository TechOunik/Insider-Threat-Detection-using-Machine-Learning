import pandas as pd
from sklearn.ensemble import IsolationForest

def train_detector():
    print("=== [STEP 3] TRAINING ISOLATION FOREST ESTIMATOR ===")
    matrix = pd.read_csv("detection_output/user_day_matrix.csv")
    feature_cols = ['off_hours_logons', 'usb_connects', 'exfil_hits', 'file_actions']
    X = matrix[feature_cols].values

    model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    matrix['anomaly_score'] = model.fit_predict(X)
    
    suspects = matrix[matrix['anomaly_score'] == -1]
    suspects.to_csv("detection_output/detected_user_days.csv", index=False)
    print(f"-> Model Trained. {len(suspects)} Anomalous User-Days Flagged.\n")

if __name__ == "__main__":
    train_detector()
