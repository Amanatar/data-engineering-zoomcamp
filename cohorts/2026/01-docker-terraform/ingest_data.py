import pandas as pd
from sqlalchemy import create_engine
import time

# Connect to database via HOST port 5433
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

def load_data():
    print("--- STARTING INGESTION ---")
    
    # 1. Load Zones
    print("Loading Zones...")
    df_zones = pd.read_csv('taxi_zone_lookup.csv')
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')
    print("Zones loaded.")

    # 2. Load Trips
    print("Loading Trips...")
    file_name = 'green_tripdata_2025-11.parquet'
    df = pd.read_parquet(file_name)
    
    # Insert schema first
    df.head(0).to_sql(name='green_taxi_trips', con=engine, if_exists='replace')
    
    # Insert data in chunks
    chunk_size = 100000
    total_rows = len(df)
    for start in range(0, total_rows, chunk_size):
        end = min(start + chunk_size, total_rows)
        chunk = df.iloc[start:end]
        chunk.to_sql(name='green_taxi_trips', con=engine, if_exists='append')
        print(f"Inserted rows {start} to {end}")

if __name__ == '__main__':
    load_data()
    print("--- INGESTION COMPLETE ---")