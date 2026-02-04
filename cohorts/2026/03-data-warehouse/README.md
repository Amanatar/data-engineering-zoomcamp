# Module 3 Homework: Data Warehousing

## Solution Approach
Since we are using a local environment without a GCP Credit Card, we used a "Hybrid Strategy":
1.  **Data Questions (Q1, Q4):** Solved using a local Python script (`solve_homework.py`) to download and process the Parquet files directly.
2.  **Theory Questions:** Solved by analyzing BigQuery architecture and documentation.

## Quiz Answers

**Question 1: Total Records 2024**
- **Answer:** `20,332,093`
- **Evidence:** Calculated via `solve_homework.py`.

**Question 2: Estimated Data Read**
- **Answer:** `0 MB for the External Table and 155.12 MB for the Materialized Table`
- **Reasoning:** External tables (GCS) do not cache metadata estimates; Native BQ tables do.

**Question 3: Columnar Storage**
- **Answer:** `BigQuery is a columnar database...`
- **Reasoning:** Querying 2 columns requires reading 2 separate file structures, increasing bytes processed.

**Question 4: Zero Fare Records**
- **Answer:** `8,333`
- **Evidence:** Calculated via `solve_homework.py`.

**Question 5: Partitioning Strategy**
- **Answer:** `Partition by tpep_dropoff_datetime and Cluster on VendorID`
- **Reasoning:** Partitioning optimizes the date filter; Clustering optimizes the sort order.

**Question 6: Partition Benefits**
- **Answer:** `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`
- **Reasoning:** Partitioning allows scanning only 15 days of data instead of 6 months.

**Question 7: External Table Storage**
- **Answer:** `GCP Bucket`

**Question 8: Always Cluster?**
- **Answer:** `False`
