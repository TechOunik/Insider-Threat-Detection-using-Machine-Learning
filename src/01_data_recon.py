import os, glob
import pandas as pd

def run_recon():
    print("=== [STEP 1] DATA RECON & POPULATION VERIFICATION ===")
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
    print(f"-> Total Population Baseline (N) : {len(pop_users)}")
    print(f"-> Verified Malicious Insiders (P): {len(gt_users)}")
    print(f"-> Verified Benign Employees     : {len(pop_users) - len(gt_users)}\n")

if __name__ == "__main__":
    run_recon()
