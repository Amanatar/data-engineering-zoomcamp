"""@bruin

name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: VendorID
    type: integer
    description: TPEP/LPEP provider code
  - name: tpep_pickup_datetime
    type: timestamp
    description: Pickup date and time
  - name: tpep_dropoff_datetime
    type: timestamp
    description: Dropoff date and time
  - name: passenger_count
    type: float
    description: Number of passengers
  - name: trip_distance
    type: float
    description: Trip distance in miles
  - name: PULocationID
    type: integer
    description: Pickup location ID
  - name: DOLocationID
    type: integer
    description: Dropoff location ID
  - name: payment_type
    type: integer
    description: Payment type code
  - name: fare_amount
    type: float
    description: Fare amount
  - name: tip_amount
    type: float
    description: Tip amount
  - name: total_amount
    type: float
    description: Total amount charged
  - name: taxi_type
    type: varchar
    description: Type of taxi (yellow or green)
  - name: extracted_at
    type: timestamp
    description: Timestamp when data was extracted

@bruin"""

import os
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

COMMON_COLUMNS = [
    "VendorID",
    "passenger_count",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "tip_amount",
    "total_amount",
]


def materialize():
    start_date = os.environ.get("BRUIN_START_DATE", "2022-01-01")
    end_date = os.environ.get("BRUIN_END_DATE", "2022-02-01")
    bruin_vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow", "green"])

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_frames = []
    current = start.replace(day=1)
    while current < end:
        year_month = current.strftime("%Y-%m")
        for taxi_type in taxi_types:
            url = f"{BASE_URL}/{taxi_type}_tripdata_{year_month}.parquet"
            print(f"Fetching: {url}")
            try:
                df = pd.read_parquet(url)

                # Normalize pickup/dropoff column names
                pickup_col = None
                dropoff_col = None
                for col in df.columns:
                    if "pickup_datetime" in col.lower():
                        pickup_col = col
                    if "dropoff_datetime" in col.lower():
                        dropoff_col = col

                if pickup_col:
                    df = df.rename(columns={pickup_col: "tpep_pickup_datetime"})
                if dropoff_col:
                    df = df.rename(columns={dropoff_col: "tpep_dropoff_datetime"})

                keep_cols = ["tpep_pickup_datetime", "tpep_dropoff_datetime"] + [
                    c for c in COMMON_COLUMNS if c in df.columns
                ]
                df = df[[c for c in keep_cols if c in df.columns]]
                df["taxi_type"] = taxi_type
                df["extracted_at"] = datetime.utcnow()
                all_frames.append(df)
                print(f"  -> {len(df)} rows")
            except Exception as e:
                print(f"  -> Skipped ({e})")

        current += relativedelta(months=1)

    if all_frames:
        result = pd.concat(all_frames, ignore_index=True)
        print(f"Total rows: {len(result)}")
        return result
    else:
        print("No data fetched")
        return pd.DataFrame()


