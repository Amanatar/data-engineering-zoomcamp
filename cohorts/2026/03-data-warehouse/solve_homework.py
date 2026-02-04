import os
import urllib.request
import pandas as pd
import pyarrow.parquet as pq

# --- CONFIGURATION ---
# We are analyzing the first 6 months of 2024 Yellow Taxi Data
MONTHS = ['01', '02', '03', '04', '05', '06']
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{}.parquet"

def process_data():
    total_records = 0
    zero_fare_records = 0

    print("--- STARTING ANALYSIS (JAN-JUN 2024) ---")
    
    for month in MONTHS:
        url = BASE_URL.format(month)
        file_name = f"yellow_tripdata_2024-{month}.parquet"
        
        print(f"Processing {file_name}...")
        
        try:
            # 1. Download the file locally
            urllib.request.urlretrieve(url, file_name)
            
            # 2. Answer Question 1: Count Total Rows
            # We use PyArrow to read metadata instantly (fast & low memory)
            table = pq.read_table(file_name)
            row_count = table.num_rows
            total_records += row_count
            
            # 3. Answer Question 4: Count Zero Fares
            # We load ONLY the 'fare_amount' column to optimize memory usage
            df = pd.read_parquet(file_name, columns=['fare_amount'])
            zero_fares = len(df[df['fare_amount'] == 0])
            zero_fare_records += zero_fares
            
            print(f"  -> Month {month}: {row_count:,} rows | {zero_fares:,} zero fares")
            
            # 4. Clean up: Remove the file to free up disk space
            os.remove(file_name)
            
        except Exception as e:
            print(f"Error on month {month}: {e}")

    # --- FINAL OUTPUT ---
    print("\n" + "="*40)
    print("FINAL HOMEWORK ANSWERS")
    print("="*40)
    print(f"Question 1 (Total Records): {total_records:,}")
    print(f"Question 4 (Zero Fare Records): {zero_fare_records:,}")
    print("="*40)

if __name__ == "__main__":
    process_data()
