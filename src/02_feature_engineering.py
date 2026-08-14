import os, glob
import pandas as pd

def build_features():
    print("=== [STEP 2] SCENARIO-MAPPED USER-DAY FEATURE EXTRACTION ===")
    data_dir = "data/raw/r4.2"
    
    # Logon
    logon_df = pd.read_csv(f"{data_dir}/logon.csv", usecols=['user', 'date', 'activity'])
    logon_df['datetime'] = pd.to_datetime(logon_df['date'])
    logon_df['day'] = logon_df['datetime'].dt.date
    logon_df['is_off_hours'] = ((logon_df['datetime'].dt.hour >= 20) | (logon_df['datetime'].dt.hour <= 6)).astype(int)
    daily_logons = logon_df.groupby(['user', 'day']).agg(
        total_logons=('activity', 'count'),
        off_hours_logons=('is_off_hours', 'sum')
    ).reset_index()

    # Device
    dev_path = f"{data_dir}/device.csv"
    if os.path.exists(dev_path):
        dev_df = pd.read_csv(dev_path, usecols=['user', 'date'])
        dev_df['day'] = pd.to_datetime(dev_df['date']).dt.date
        daily_devices = dev_df.groupby(['user', 'day']).size().reset_index(name='usb_connects')
    else: daily_devices = pd.DataFrame(columns=['user', 'day', 'usb_connects'])

    # HTTP
    http_path = f"{data_dir}/http.csv"
    http_chunks = []
    if os.path.exists(http_path):
        for chunk in pd.read_csv(http_path, usecols=['user', 'date', 'url'], chunksize=1000000):
            chunk['day'] = pd.to_datetime(chunk['date']).dt.date
            susp = chunk[chunk['url'].str.contains('wikileaks|dropbox|job|monster|indeed|keylogger|upload|mega', case=False, na=False)]
            if not susp.empty: http_chunks.append(susp.groupby(['user', 'day']).size().reset_index(name='exfil_hits'))
        daily_http = pd.concat(http_chunks).groupby(['user', 'day'])['exfil_hits'].sum().reset_index() if http_chunks else pd.DataFrame(columns=['user', 'day', 'exfil_hits'])
    else: daily_http = pd.DataFrame(columns=['user', 'day', 'exfil_hits'])

    # File
    file_path = f"{data_dir}/file.csv"
    if os.path.exists(file_path):
        file_df = pd.read_csv(file_path, usecols=['user', 'date'])
        file_df['day'] = pd.to_datetime(file_df['date']).dt.date
        daily_files = file_df.groupby(['user', 'day']).size().reset_index(name='file_actions')
    else: daily_files = pd.DataFrame(columns=['user', 'day', 'file_actions'])

    # Merge
    matrix = pd.merge(daily_logons, daily_devices, on=['user', 'day'], how='left')
    matrix = pd.merge(matrix, daily_http, on=['user', 'day'], how='left')
    matrix = pd.merge(matrix, daily_files, on=['user', 'day'], how='left').fillna(0)
    
    os.makedirs("detection_output", exist_ok=True)
    matrix.to_csv("detection_output/user_day_matrix.csv", index=False)
    print(f"-> Successfully Generated User-Day Feature Matrix: {len(matrix)} rows saved.\n")

if __name__ == "__main__":
    build_features()
