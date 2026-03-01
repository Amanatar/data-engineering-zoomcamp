# Module 5 Homework: Data Platforms with Bruin

## Answers

| # | Question | Answer |
|---|----------|--------|
| **Q1** | Bruin Pipeline Structure | `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/` |
| **Q2** | Materialization Strategies | `time_interval` - incremental based on a time column |
| **Q3** | Pipeline Variables | `bruin run --var 'taxi_types=["yellow"]'` |
| **Q4** | Running with Dependencies | `bruin run --select ingestion.trips+` |
| **Q5** | Quality Checks | `name: not_null` |
| **Q6** | Lineage and Dependencies | `bruin lineage` |
| **Q7** | First-Time Run | `--full-refresh` |

## Pipeline Run Results

```
bruin run completed successfully in 17.767s

 ✓ Assets executed      4 succeeded
 ✓ Quality checks       10 succeeded
```

### Row Counts
| Table | Rows |
|-------|------|
| ingestion.trips | 2,463,931 |
| staging.trips | 2,452,509 |
| reports.trips_report | 156 |
| ingestion.payment_lookup | 7 |

## Pipeline Structure

```
my-pipeline/
├── .bruin.yml                              # DuckDB connection config
└── pipeline/
    ├── pipeline.yml                        # Pipeline name, schedule, variables
    └── assets/
        ├── ingestion/
        │   ├── trips.py                    # Python ingestion (NYC taxi parquet)
        │   ├── requirements.txt            # pandas, requests, pyarrow
        │   ├── payment_lookup.asset.yml    # Seed asset
        │   └── payment_lookup.csv          # Lookup data
        ├── staging/
        │   └── trips.sql                   # Deduplicate + enrich + time_interval
        └── reports/
            └── trips_report.sql            # Aggregation by date/taxi/payment
```
