import pandas as pd
from sqlalchemy import create_engine

# Connect to database
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

def run_query(q_num, query):
    print(f"\n=== ANSWER FOR QUESTION {q_num} ===")
    try:
        df = pd.read_sql(query, engine)
        print(df.to_string(index=False))
    except Exception as e:
        print(e)

# Q3: Count short trips
q3 = """
SELECT count(*) as "Trip Count"
FROM green_taxi_trips 
WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01' 
  AND trip_distance <= 1.0;
"""

# Q4: Longest trip day
q4 = """
SELECT DATE(lpep_pickup_datetime) as "Day with Longest Trip", trip_distance
FROM green_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
"""

# Q5: Biggest pickup zone on Nov 18
q5 = """
SELECT z."Zone" as "Top Zone", SUM(t.total_amount) as "Total Amount"
FROM green_taxi_trips t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY "Total Amount" DESC
LIMIT 1;
"""

# Q6: Largest tip dropoff zone
q6 = """
SELECT z_drop."Zone" as "Dropoff Zone w/ Highest Tip", t.tip_amount
FROM green_taxi_trips t
JOIN zones z_pick ON t."PULocationID" = z_pick."LocationID"
JOIN zones z_drop ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01' AND t.lpep_pickup_datetime < '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;
"""

run_query(3, q3)
run_query(4, q4)
run_query(5, q5)
run_query(6, q6)