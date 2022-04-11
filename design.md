# Design Tips and Techniques


----
### Designing keys in a key-value store
__

Design the key as: `Object:ID:Attribute`

Example:

    User:3:groups  ->  [5, 6, 7, 12]
    User:3:prefs   ->  {notifs:yes, area:51}
..


----
### Designing BigTable RowKey for Last N queries
__

tdlr: Use reverse timestamps

Last N queries apply when finding the most rececent max/min/avg values
in a window over some data stream

Google BigTable is sorted lexicographically the RowKey.

If the RowKey is such that the newest record is placed first, then the
table scan is much faster.

Adding a reverse timestamp to the RowKey, which decreases in value over
time, will place newer records first.

Java Reverse Timestamp:
    java.lang.Long.MAX_VALUE - ts.getMillis()

Python3:
    sys.maxsize - int(time.time()*1000*1000)
..


----
### Handling Missing Values
__

- Clarify the meaning of missing data to decide what to do with it
- Know the business domain to inform the meaning

- Examples:
    - Questionaires have missing values toward the last questions
        - because participants got tired and stopped participating.
    - Sales data. Days since previous order has missing values.
        - Normal because new customers will now have previous orders

- Standard Techniques:
    - Re-extract the data if the dataset is too messy/inconsistent
    - Remove the record
    - Impute missing values with mean/median/mode
        - If not a lot of missing data
    - Model missing value
    - Drop column
    - Drop rows
        - If data is important and lots of rows and few missing data

- See: Data Cleaning: Types of Missing Values and How to Handle Them
    - https://www.youtube.com/watch?v=QLjv3IQ6hrs&t=51s
..


----
### New Data Source Checklist
__

- Check for duplicate rows
- Check missing values found in columns
..


----
### Design optimal production pipelines
__

- Revisit the schema
    - Has the goals changed

- Revisit the data
    - Data skew
..


----
### Performance Checklist
__

- Query Access Patterns
- Data Skew
- CPU Load
- Memory Bottlenecks
- Storage Bottlenecks (SSD over HDD)
- Network Chain from Client to Server
- Replicate, then separate read and write
..


----
### Efficiency Checklist
__

- I/O
    - How many bytes were read from disk
- Shuffling
    - How many bytes were passed to the next stage
- Grouping
    - How many bytes were passed through to each group
- Materialization
    - How many bytes were written permanently out to disk
- Functions and UDFs
    - How much CPU were consumed by the functions
..


----
### SQL Query Optimization Checklist
__

- Avoid SELECT *
- Use built-in functions
- Use WHERE clause to filter out early and often
- Use ORDER only on the outermost query
- Put larger table on the left of a JOIN
- Use GROUP BY only for low cardinality columns
- Always include a partition filter
- Use EXPLAIN
- Monitor query performance

- Use materialized results if commonly computed
    - Compare cost of storing data vs processing data
..


----
### Physical Database Design
__

- Schema:
    - Partition tables typically by day
    - Cluster columns where applicable
..


