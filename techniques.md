# Data Techniques


----
### Sample 1 out of 1000 rows
__

tldr: Compute the hash of column as numeric, MOD it and pick one value.

```
SELECT
    # Technique to sample 1 out of 1000 rows
    MOD(ABS(FARM_FINGERPRINT(CAST(pickup_datetime AS STRING))),1000) = 1
```
..


----
### Lock the label variable, spread features by deciles
__ Sample Query

# Relate departure_delay to arrival delays

%%bigquery df
SELECT
  departure_delay,
  COUNT(1) AS num_flights,
  APPROX_QUANTILES(arrival_delay, 10) AS arrival_delay_deciles
FROM
  `bigquery-samples.airline_ontime_data.flights`
GROUP BY
  departure_delay
HAVING
  num_flights > 100
ORDER BY
  departure_delay ASC
..


----
### BigQuery: Get typical value of a column
__ Typical trip duration

tldr: Use APPROX_QUANTILES(column,10)[OFFSET (5)]

# Query to get typical trip duration
-- CREATE OR REPLACE TABLE mydataset.typical_trip AS
SELECT
  start_station_name,
  end_station_name,
  APPROX_QUANTILES(duration, 10)[OFFSET (5)] AS typical_duration,
  COUNT(duration) AS num_trips
FROM
  `bigquery-public-data`.london_bicycles.cycle_hire
GROUP BY
  start_station_name,
  end_station_name

- See: https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles
..
__ Days when trips are longer than usual

# Save query above into mydataset.typical_trip

SELECT
  EXTRACT (DATE FROM start_date) AS trip_date,
  APPROX_QUANTILES(duration / typical_duration, 10)[OFFSET(5)] AS ratio,
  COUNT(*) AS num_trips_on_day
FROM
  `bigquery-public-data`.london_bicycles.cycle_hire AS hire
JOIN
  mydataset.typical_trip AS trip
ON
  hire.start_station_name = trip.start_station_name
  AND hire.end_station_name = trip.end_station_name
  AND num_trips > 10
GROUP BY
  trip_date
HAVING
  num_trips_on_day > 10
ORDER BY
  ratio DESC
LIMIT
  10
..


----
### Avoid self-joins to large tables:
__ Don't do this:

WITH

male_babies AS (
    SELECT name,
           number AS num_babies
      FROM `bigquery-public-data`.usa_names.usa_1910_current
     WHERE gender = 'M'
),

female_babies AS (
    SELECT name,
           number AS num_babies
      FROM `bigquery-public-data`.usa_names.usa_1910_current
     WHERE gender = 'F'
),

both_genders AS (
SELECT name,
       SUM(m.num_babies) + SUM(f.num_babies) AS num_babies,
       SUM(m.num_babies) / (SUM(m.num_babies) + SUM(f.num_babies)) AS frac_male
  FROM male_babies AS m JOIN female_babies AS f USING (name)
 GROUP BY name
)

SELECT *
  FROM both_genders
 WHERE frac_male BETWEEN 0.3 AND 0.7
ORDER BY num_babies DESC
LIMIT 5
..
__ Do this instead:

WITH

all_babies AS (
    SELECT name,
           SUM( IF(gender = 'M', number, 0)) AS male_babies,
           SUM( IF(gender = 'F', number, 0)) AS female_babies
     FROM `bigquery-public-data.usa_names.usa_1910_current`
     GROUP BY  name
),

both_genders AS (
    SELECT name,
           (male_babies + female_babies) AS num_babies,
           SAFE_DIVIDE(male_babies, male_babies + female_babies) AS frac_male
      FROM all_babies
     WHERE male_babies > 0 AND female_babies > 0
)

SELECT *
  FROM both_genders
 WHERE frac_male BETWEEN 0.3 AND 0.7
 ORDER BY num_babies DESC
 LIMIT 5
..


----
### Use LEAD() or LAG() window functions to avoid joins
__ Do this:

# Find duration between a bike being dropped off and it being rented again:
SELECT
  bike_id,
  start_date,
  end_date,
  TIMESTAMP_DIFF( start_date, LAG(end_date) OVER (PARTITION BY bike_id ORDER BY start_date), SECOND) AS time_at_station
FROM `bigquery-public-data`.london_bicycles.cycle_hire
LIMIT 5
..


----
### Distribute large sorts over several workers
__ Don't do this:

# Bad: Sorting done on a single worker
SELECT
  rental_id,
  ROW_NUMBER() OVER(ORDER BY end_date) AS rental_number
FROM
  `bigquery-public-data.london_bicycles.cycle_hire`
ORDER BY rental_number ASC
LIMIT 5
..
__ Do this instead:

# Better: Sorting within a single day can be distributed
# Partition by rental_date first
WITH
  rentals_on_day AS (
  SELECT
    rental_id,
    end_date,
    EXTRACT(DATE
    FROM
      end_date) AS rental_date
  FROM
    `bigquery-public-data.london_bicycles.cycle_hire` )
SELECT
  rental_id,
  rental_date,
  ROW_NUMBER() OVER(PARTITION BY rental_date ORDER BY end_date) AS rental_number_on_day
FROM
  rentals_on_day
ORDER BY
  rental_date ASC,
  rental_number_on_day ASC
LIMIT 5
..


----
### Distribute GROUP BY using a pseudo-column
__ Don't do this:

# Query fails with 'Cannot query rows larger than 100MB limit
SELECT
  author.tz_offset,
  ARRAY_AGG(STRUCT(author,
      committer,
      subject,
      message,
      trailer,
      difference,
      encoding)
  ORDER BY
    author.date.seconds)
FROM
  `bigquery-public-data.github_repos.commits`
GROUP BY
  author.tz_offset
..
__ Do this instead:

# Add another column to GROUP BY then regroup
SELECT
  repo_name,
  author.tz_offset,
  ARRAY_AGG(STRUCT(author,
      committer,
      subject,
      message,
      trailer,
      difference,
      encoding)
  ORDER BY
    author.date.seconds)
FROM
  `bigquery-public-data.github_repos.commits`,
  UNNEST(repo_name) AS repo_name
GROUP BY
  repo_name,
  author.tz_offset )
..


----
### Locate Missing Data
__

import pandas as pd
import numpy as np

data = pd.read_csv('source.csv')

data.isnull()

data.isnull().any()

data.isnull().sum()

..

----
### Locate Duplicates
__

import pandas as pd

data = pd.read_csv("source.csv")

data.duplicated()                                   # Find dups

data.drop_duplicates()                              # Drop dups
..


----
### Use the missingno package
__ https://github.com/ResidentMario/missingno
..


----
#### Standardize casing
__

data['Column_1'] = data['Column_1'].str.lower()
data['Column_2'] = data['Column_2'].str.title()

..

