/* @bruin

name: reports.trips_report
type: duckdb.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

columns:
  - name: pickup_date
    type: date
    description: Date of trip pickup
    primary_key: true
    checks:
      - name: not_null
  - name: taxi_type
    type: varchar
    description: Type of taxi (yellow/green)
    primary_key: true
    checks:
      - name: not_null
  - name: payment_type_name
    type: varchar
    description: Payment type description
    primary_key: true
  - name: trip_count
    type: bigint
    description: Number of trips
    checks:
      - name: non_negative
  - name: total_passengers
    type: float
    description: Total number of passengers
  - name: avg_trip_distance
    type: float
    description: Average trip distance
  - name: total_fare
    type: float
    description: Total fare amount
  - name: total_tips
    type: float
    description: Total tip amount
  - name: total_revenue
    type: float
    description: Total revenue (fare + tips)

@bruin */

SELECT
    CAST(pickup_datetime AS DATE) AS pickup_date,
    taxi_type,
    payment_type_name,
    COUNT(*) AS trip_count,
    SUM(passenger_count) AS total_passengers,
    AVG(trip_distance) AS avg_trip_distance,
    SUM(fare_amount) AS total_fare,
    SUM(tip_amount) AS total_tips,
    SUM(total_amount) AS total_revenue
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY
    CAST(pickup_datetime AS DATE),
    taxi_type,
    payment_type_name
