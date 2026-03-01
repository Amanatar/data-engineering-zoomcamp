/* @bruin

name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: pickup_datetime
    type: timestamp
    description: Pickup date and time
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: Dropoff date and time
  - name: taxi_type
    type: varchar
    description: Type of taxi
    primary_key: true
    checks:
      - name: not_null
  - name: passenger_count
    type: float
    description: Number of passengers
  - name: trip_distance
    type: float
    description: Trip distance in miles
    checks:
      - name: non_negative
  - name: pu_location_id
    type: integer
    description: Pickup location ID
    primary_key: true
  - name: do_location_id
    type: integer
    description: Dropoff location ID
    primary_key: true
  - name: payment_type
    type: integer
    description: Payment type code
  - name: payment_type_name
    type: varchar
    description: Payment type description
  - name: fare_amount
    type: float
    description: Fare amount
  - name: tip_amount
    type: float
    description: Tip amount
  - name: total_amount
    type: float
    description: Total amount charged

custom_checks:
  - name: no_duplicate_trips
    description: Ensure no duplicate trips after deduplication
    query: |
      SELECT COUNT(*) - COUNT(DISTINCT (pickup_datetime, dropoff_datetime, pu_location_id, do_location_id, taxi_type))
      FROM staging.trips
      WHERE pickup_datetime >= '{{ start_datetime }}'
        AND pickup_datetime < '{{ end_datetime }}'
    value: 0

@bruin */

SELECT
    t.tpep_pickup_datetime AS pickup_datetime,
    t.tpep_dropoff_datetime AS dropoff_datetime,
    t.taxi_type,
    t.passenger_count,
    t.trip_distance,
    t.pu_location_id,
    t.do_location_id,
    t.payment_type,
    p.payment_type_name,
    t.fare_amount,
    t.tip_amount,
    t.total_amount
FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY tpep_pickup_datetime, tpep_dropoff_datetime, pu_location_id, do_location_id, taxi_type
            ORDER BY extracted_at DESC
        ) AS rn
    FROM ingestion.trips
    WHERE tpep_pickup_datetime >= '{{ start_datetime }}'
      AND tpep_pickup_datetime < '{{ end_datetime }}'
) t
LEFT JOIN ingestion.payment_lookup p
    ON t.payment_type = p.payment_type_id
WHERE t.rn = 1
  AND t.tpep_pickup_datetime IS NOT NULL
