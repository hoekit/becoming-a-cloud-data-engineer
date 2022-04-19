# TODO
<small>Things to do that'll enhance the Cloud Data Engineering journey</small>


----
### End-to-end Kafka, Flink, InfluxDB, Grafana
__ Steps

1. Create a pseudo data generator in Python/Scala that writes to CSV or
   JSONL

2. Modify the data generator to write to Kafka

3. Create an Flink job that consumes the data in a style similar to the
   Kafka Deep Dive and stores the data in JSONL or CSV

4. Modify the Flink job to write data to InfluxDB

5. Create a Grafana visualization display to show data in InfluxDB

6. Create a separate Flink job that uses Event_Time instead of
   Processing_Time. This uses the Lambda Architecture.
..
__ Links

- Tutorial: Processing Kafka Sources and Sinks with Apache Flink in Python
    - https://thecodinginterface.com/blog/kafka-source-sink-with-apache-flink-table-api/

- Flink Deep Dive - Concepts and Real Examples
    - https://www.youtube.com/watch?v=_8fHV5woDtQ
..

----
### Unsorted
__ Unsorted

- Would be nice to compare the features of Dataflow/Apache Beam and how
  the equivalent is achieved in Apache Spark or other solutions
    - Or maybe do a proper search on the web and collect in one place,
      everything related to them and write up an article

- Study the flow in this Apache Beam analytics project:
    - https://www.youtube.com/watch?v=dPuE30kY6-c
    - Design and create a platform that can handle auto-production and
      broadcasting, for up to hundreds of games per weekend with as
      little time delay as possible

- Create a Data Quality Cheatsheet
    - Start by collecting the tips in DQ in BigQuery. [web](https://www.cloudskillsboost.google/course_sessions/905155/video/115842)
    - Extend as needed.
..
