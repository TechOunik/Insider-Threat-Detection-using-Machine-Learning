import pandas as pd

INPUT_FILE = '/home/obioma/Documents/FYProject/data/raw/r4.2/logon.csv'

def profile_24h_behaviour():
    print("--- Initialising 24-Hour Behavioural Profiler ---")
    chunk_iterator = pd.read_csv(INPUT_FILE, chunksize=100000)
    
    daily_profiles = []

    for chunk in chunk_iterator:
        chunk['date'] = pd.to_datetime(chunk['date'])
        
        # Create a 'Day' column to group by
        chunk['day'] = chunk['date'].dt.date
        
        # Count activity per user, per day, across the full 24 hours
        summary = chunk.groupby(['user', 'day']).size().reset_index(name='activity_count')
        
        daily_profiles.append(summary)
        print(f"Processed chunk... monitoring 24h cycles.")

    # Combine all chunks and sum up the activity
    final_profiles = pd.concat(daily_profiles).groupby(['user', 'day']).sum().reset_index()
    
    # Identify 'Statistical Outliers' (People doing way more than average)
    threshold = final_profiles['activity_count'].mean() + (2 * final_profiles['activity_count'].std())
    anomalies = final_profiles[final_profiles['activity_count'] > threshold]

    print(f"\n--- 24-Hour Analysis Complete ---")
    print(f"Average daily activity: {final_profiles['activity_count'].mean():.2f}")
    print(f"High-intensity anomalies detected: {len(anomalies)}")
    
    return anomalies

if __name__ == "__main__":
    profile_24h_behaviour()
