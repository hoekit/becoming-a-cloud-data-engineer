# Batch Analytics with Beam Cloud Dataflow

----

__ Steps

1. Write a pipeline that aggregates site traffic by user

2. Write a pipeline that aggregates site traffic by minute

3. Implement windowing on time series data
..

__ Setup

- Download dependencies
    ```
        # Change directory into the lab
        cd 3_Batch_Analytics/labs
        # Download dependencies
        mvn clean dependency:resolve
        export BASE_DIR=$(pwd)
    ```

- Setup data environment
    ```
        cd $BASE_DIR/../..
        source create_batch_sinks.sh
        source generate_batch_events.sh
        cd $BASE_DIR
    ```

- Script creates events like:
    ```
        {"user_id": "-6434255326544341291",
         "ip": "192.175.49.116",
         "timestamp": "2019-06-19T16:06:45.118306Z",
         "http_request": "\"GET eucharya.html HTTP/1.0\"",
         "lat": 37.751,
         "lng": -97.822,
         "http_response": 200,
         "user_agent":"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.01; Trident/5.1)",
         "num_bytes": 182
        }
    ```

- Events are copied to `gs://my-project-id/events.json`

..

__ Aggregate site traffic by user

- Links:
    - [1] https://beam.apache.org/releases/javadoc/2.22.0/index.html?org/apache/beam/sdk/transforms/Sum.html
    - [2] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/transforms/Count.html
    -[3] https://beam.apache.org/releases/javadoc/2.22.0/index.html?org/apache/beam/sdk/transforms/Combine.html
..

__ Aggregate site traffic by minute

- Events already have a timestamp so extract via the `WithTimestamps`[1] transform

- Links
    - [1] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/transforms/WithTimestamps.html

..
