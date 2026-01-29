# Module 2 Homework Solutions

## Quiz Answers

**Question 1: File Size**
- Answer: **128.3 MiB**
- Logic: Verified using `ls -lh` in Kestra flow `01-quiz-file-size`.

**Question 2: Variable Substitution**
- Answer: **green_tripdata_2020-04.csv**
- Logic: Replaced `{{inputs.taxi}}` with 'green' and dates accordingly.

**Question 3: Yellow Taxi 2020 Rows**
- Answer: **24,648,499**
- Logic: Calculated using Python streaming script in flow `02-quiz-row-counter`.

**Question 4: Green Taxi 2020 Rows**
- Answer: **1,734,051**
- Logic: Calculated using Python streaming script in flow `02-quiz-row-counter`.

**Question 5: Yellow Taxi March 2021 Rows**
- Answer: **1,925,152**
- Logic: Extracted from logs of `02-quiz-row-counter` (Month 03).

**Question 6: Timezone Configuration**
- Answer: **Add a `timezone` property set to `America/New_York`**
- Logic: Kestra uses IANA timezones (Region/City) to handle Daylight Saving Time correctly. Fixed offsets like EST or UTC-5 do not adjust for DST.
