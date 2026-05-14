import pandas as pd

INPUT_FILE = '/home/obioma/Documents/FYProject/data/raw/r4.2/email.csv'
OUTPUT_FILE = '/home/obioma/Documents/FYProject/data/processed/suspicious_emails.csv'

def analyse_email_stream():
    print("--- Initialising Email Exfiltration Analyser ---")
    # Using specific columns to save RAM
    cols = ['date', 'user', 'to', 'attachments']
    chunk_iterator = pd.read_csv(INPUT_FILE, usecols=cols, chunksize=100000)
    
    suspicious_emails = []

    for i, chunk in enumerate(chunk_iterator):
        # 1. Identify External Recipients
        # We look for anyone NOT receiving mail at the company domain '@dante.com'
        external = chunk[~chunk['to'].str.contains('@dante.com', na=False)]
        
        # 2. Identify Emails with Attachments
        # In this dataset, 0 means no attachment. We want > 0.
        with_files = external[external['attachments'] > 0]
        
        suspicious_emails.append(with_files)
        print(f"Chunk {i+1}: Found {len(with_files)} external emails with attachments.")

    # Combine the 'Signal'
    signal_df = pd.concat(suspicious_emails)
    signal_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n--- Email Analysis Complete ---")
    print(f"Total Suspicious External Emails: {len(signal_df)}")
    return signal_df

if __name__ == "__main__":
    analyse_email_stream()
