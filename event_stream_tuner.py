import pandas as pd
import os

# Configuration
INPUT_FILE = '/home/obioma/Documents/FYProject/data/raw/r4.2/logon.csv'
OUTPUT_FILE = '/home/obioma/Documents/FYProject/data/processed/high_signal_logons.csv'

def tune_event_stream():
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # We only need these columns for behavioural analysis
    relevant_cols = ['date', 'user', 'activity']
    
    print("--- Initialising Event Stream Tuner ---")
    chunk_iterator = pd.read_csv(INPUT_FILE, usecols=relevant_cols, chunksize=100000)
    
    high_signal_list = []

    for i, chunk in enumerate(chunk_iterator):
        # Convert date to datetime objects
        chunk['date'] = pd.to_datetime(chunk['date'])
        
        # JAY JAY'S ADVICE: Filter for 'Relevant' events
        # Focus: After-hours activity (Before 07:00 or after 19:00)
        after_hours = chunk[(chunk['date'].dt.hour < 7) | (chunk['date'].dt.hour > 19)]
        
        # Focus: Successful logons during these suspicious times
        logon_events = after_hours[after_hours['activity'] == 'Logon']
        
        high_signal_list.append(logon_events)
        print(f"Chunk {i+1}: Isolated {len(logon_events)} high-signal events.")

    # Combine and save the filtered "Signal"
    signal_df = pd.concat(high_signal_list)
    signal_df.to_csv(OUTPUT_FILE, index=False)
    
    print("\n--- Tuning Complete ---")
    print(f"Total High-Signal Events isolated: {len(signal_df)}")
    print(f"Filtered data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    tune_event_stream()
