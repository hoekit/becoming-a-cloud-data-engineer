# BEAM Batch Analytics in Python

__ Setup

- IDE: Use the Vertex AI > Workbench > New Notebook

- Git Repo:
    - git clone https://github.com/GoogleCloudPlatform/training-data-analyst
    - cd ~/project/training-data-analyst/quests/dataflow_python/

```
    PROJECT_ID=$(gcloud config get-value project)
    export PROJECT_NUMBER=$(gcloud projects list --filter="$PROJECT_ID" --format="value(PROJECT_NUMBER)")
    export serviceAccount=""$PROJECT_NUMBER"-compute@developer.gserviceaccount.com"
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:${serviceAccount}" --role="roles/dataflow.worker"
```

- Setup Python
    ```
        sudo apt-get install -y python3-venv
        ## Create and activate virtual environment
        python3 -m venv df-env
        source df-env/bin/activate
        python3 -m pip install -q --upgrade pip setuptools wheel
        python3 -m pip install apache-beam[gcp]
    ```

..

----
### Aggregate By User

__ Scope

1. Sum page views per user
..

__ Steps

1. Read data into Beam

2. Aggregate by user, count page_views and sum num bytes

3. Write to Output
..

__ Detailed Steps

1. Create a run() function that runs when called as script

2. Implement run()
    - Add an ArgumentParser
        - Store parsed arguments into `opts`
    - Use `opts` to configure the Beam PipelineOptions
    - Create a pipeline from PipelineOptions
    - Define pipeline componnents
        - Read from path (Google Cloud Storage)
        - Parse each line into CommonLog string
            - Define the `CommonLog` NamedTuple[1] class
            - Define `parse_json` parsing helper function
            - Do user aggregation
                - Output to a `PerUserAggregation` NamedTuple
                - Define class for `PerUserAggregation`
                - Define function CountCombineFn() [2]
                - Aggregate using Count
            - Convert to dictionary
                - Use the _asdict() function[3]
            - Write to file
                - Write to text file
    - Setup source and sink
        - source: type=file, name=`input_path`
        - sink: type=BigQuery_table, name=`output_table`

- Links
    - [1] https://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python
    - [2] https://beam.apache.org/releases/pydoc/2.28.0/apache_beam.transforms.combiners.html#apache_beam.transforms.combiners.Count
    - [3] https://stackoverflow.com/questions/26180528/convert-a-namedtuple-into-a-dictionary
..


----
### Aggregate By Minute

__ Scope

1. Aggregate metrics by one-minute windows
..

__ Steps

1. Read data into Beam

2. Setup one-minute windows

3. Aggregte metrics

4. Write to Output
..

__ Detailed Steps

1. Setup `run()` function
    - Setup argument parser
    - Setup pipeline options and create pipeline
    - Create pipeline components
        - Read from local text file
        - Create a timestamped element
            - Use the strptime[1] function of the datetime[2] package
        - Window into one-minute windows
        - Write to local text file

- Links
    - [1] https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    - [2] https://docs.python.org/3/library/datetime.html
..

