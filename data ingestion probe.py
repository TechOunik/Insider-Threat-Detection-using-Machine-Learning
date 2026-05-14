import pandas as pd

# Path to your CERT data
LOGON_FILE = '/home/obioma/Documents/FYProject/data/raw/r4.2/logon.csv'

def process_logons_lightweight(file_path):
    # Using a chunksize of 100k rows to keep RAM usage low
    chunk_iterator = pd.read_csv(file_path, chunksize=100000)
    
    total_processed = 0
    print("--- Starting Lightweight Ingestion ---")
    
    for chunk in chunk_iterator:
        # Standardise timestamps to datetime objects
        chunk['date'] = pd.to_datetime(chunk['date'])
        
        # Example Feature: Count logons per user
        user_counts = chunk['user'].value_counts()
        
        total_processed += len(chunk)
        print(f"Processed {total_processed} events...")
        
        # Here is where we will eventually add the '6-hour window' logic
        
    print("--- Ingestion Complete ---")

if __name__ == "__main__":
    process_logons_lightweight(LOGON_FILE)
