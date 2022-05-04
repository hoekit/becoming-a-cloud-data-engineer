# Java Batch ETL Pipeline using Apache Beam and Cloud Dataflow


----

__ **Setup**

- Setup Theia IDE [1]
    - Supports `gcloud` out-of-the-box

- Links
    - [1] https://theia-ide.org/
..

__ **Steps**

0. Lab URL [1]

1. Understand the input data

2. Read input data

3. Transform input data

4. Write transformed data to BigQuery

5. Use a similar pipeline from Dataflow Template

- Links
    - [1] https://github.com/GoogleCloudPlatform/training-data-analyst/tree/master/quests/dataflow/1_Basic_ETL/labs
..

__ **Understand the input data**

- Input data is a JSONL file and the pipeline should emit web server
  logs in Common Log Format [1]

- Data treated as batch source

- Links
    - [1] https://en.wikipedia.org/wiki/Common_Log_Format
..

__ **Setup the Project**

- Github link to lab [1]

- Edit the dependencies in the Maven pom.xml file
    - Add dependencies on Apache Beam

```
    <!-- Apache BEAM -->
    <dependency>
      <groupId>org.apache.beam</groupId>
      <artifactId>beam-sdks-java-core</artifactId>
      <version>${beam.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.beam</groupId>
      <artifactId>beam-runners-direct-java</artifactId>
      <version>${beam.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.beam</groupId>
      <artifactId>beam-sdks-java-io-google-cloud-platform</artifactId>
      <version>${beam.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.beam</groupId>
      <artifactId>beam-runners-google-cloud-dataflow-java</artifactId>
      <version>${beam.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.beam</groupId>
      <artifactId>beam-sdks-java-extensions-google-cloud-platform-core</artifactId>
      <version>${beam.version}</version>
    </dependency>
```

- Be sure to check the beam.version in the `properties` tag

```
  <properties>
    <!-- Dependency properties -->
    <beam.version>2.32.0</beam.version>
    ...
```

- Download the dependencies
    - `mvn clean dependency:resolve`

- Clone repo containing scripts to generate synthetic web server logs
    ```
        cd $BASE_DIR/../..

        # Create GCS buckets and BQ dataset
        source create_batch_sinks.sh

        # Generate a batch of web server log events
        bash generate_batch_events.sh

        # View events
        head events.json

        # Sample event
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

- Links
    - [1] https://github.com/GoogleCloudPlatform/training-data-analyst/tree/master/quests/dataflow/1_Basic_ETL/labs

..

__ **Read data**

- Create a single class for the pipeline called `MyPipeline`
    - `public class MyPipeline {...}`

- Create an `Options` interface in `MyPipeline`
    - `public interface Options extends DataflowPipelineOptions {...}`

- Create a `main` method in `MyPipeline`
    - `public static void main(String[] args) {...}`

- Create a `run` method in `MyPipeline`
    - `public static PipelineResult run(Options options) {...}`
    - The pipeline[1] is created in this method using pipeline options[2]:
        - `Pipeline pipeline = Pipeline.create(options);`
    - And ran:
        - `return pipeline.run();`

- Next get the input data into a PCollection[3]:
    - `pipeline.apply("ReadLines", TextIO.read().from(...));`

- Try running the pipeline using DirectRunner:
    ```
        cd $BASE_DIR
        export MAIN_CLASS_NAME=com.mypackage.pipeline.MyPipeline
        mvn compile exec:java -Dexec.mainClass=${MAIN_CLASS_NAME}

    ```

- Links
    - [1] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/Pipeline.html
    - [2] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/options/PipelineOptions.html
    - [3] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/values/PCollection.html
    - [4] https://beam.apache.org/documentation/runners/direct/
..

__ **Transform data**

- Sequential (i.e. non-branching) transforms[1] can be chained like JS
    ```
        [Final Output PCollection] = [Initial Input PCollection]
            .apply([First Transform])
            .apply([Second Transform])
            .apply([Third Transform]);
    ```

- This transform uses a ParDo[2] transform that parses the data using
  Gson[3]

- ParDo functions can call DoFn[4] inline or as a static class.

- Inline ParDo example:
    ```
        // @ProcessElement and @Element requires
        // import org.apache.beam.sdk.schemas.annotations.DefaultSchema;
        pCollection.apply(ParDo.of(new DoFn<T1, T2>() {
            @ProcessElement
            public void processElement(@Element T1 i, OutputReceiver<T2> r) {
                // Do something
                r.output(0);
            }
        }));
    ```

- Static Class ParDo example:
    ```
        static class MyDoFn extends DoFn<T1, T2> {
            @ProcessElement
            public void processElement(@Element T1 json, OutputReceiver<T2> r)
                    throws Exception {
                // Do something
                r.output(0);
            }
        }

        pCollection.apply(ParDo.of(new MyDoFn()));
    ```

- Using Gson to convert JSON into strongly typed object:
    ```
        // Somewhere
        @DefaultSchema(JavaFieldSchema.class)
        class MyClass {
            int field1;
            String field2;
        }

        // Within DoFn
        Gson gson = new Gson();
        MyClass myClass = gson.fromJson(jsonString, MyClass);

    ```

- Mapping BigQuery types to Java types:
    - BQ:STRING  -- J:String
    - BQ:FLOAT   -- J:Double
    - BQ:INTEGER -- J:Long

- Sample `events.json` line:
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


- Links
    - [1] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/transforms/PTransform.html
    - [2] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/transforms/ParDo.html
    - [3] https://github.com/google/gson
    - [4] https://beam.apache.org/releases/javadoc/2.22.0/org/apache/beam/sdk/transforms/DoFn.html
..

