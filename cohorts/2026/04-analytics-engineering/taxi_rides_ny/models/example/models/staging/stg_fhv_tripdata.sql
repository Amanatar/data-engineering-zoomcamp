{{ config(materialized='view') }}

select
    dispatching_base_num,
    cast(PULocationID as integer) as pickup_location_id,
    cast(DOLocationID as integer) as dropoff_location_id,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    sr_flag,
    affinity_code

from {{ source('staging', 'fhv_tripdata') }}
where dispatching_base_num is not null 
  and extract(year from pickup_datetime) = 2019