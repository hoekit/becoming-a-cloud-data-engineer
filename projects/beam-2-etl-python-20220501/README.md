# Python Batch ETL Pipeline using Apache Beam and Cloud Dataflow

----

__ Setup

- Access Theia IDE (beta) via Vertex AI > Workbench

- Download code repo (1.5GB)
    - `git clone https://github.com/GoogleCloudPlatform/training-data-analyst`
    - `cd ~/project/training-data-analyst/quests/dataflow_python/`

- Lab Folder
    - `cd 1_Basic_ETL/lab`
    - `export BASE_DIR=$(pwd)`

- Setup virtual environment
    ```
        sudo apt-get install -y python3-venv
        python3 -m venv df-env
        source df-env/bin/activate
    ```

- Install required packages
    ```
        python3 -m pip install -q --upgrade pip setuptools wheel
        python3 -m pip install apache-beam[gcp]
    ```

- Enable Dataflow API
    ```
        gcloud services enable dataflow.googleapis.com
    ```

- Generate synthetic data
    ```
        cd $BASE_DIR/../..
        source create_batch_sinks.sh
        bash generate_batch_events.sh
        head events.json
    ```
..

__ Read Data

- Import required modules
    ```
        import argparse
        import time
        import logging
        import json
        import apache_beam as beam
        from apache_beam.options.pipeline_options import GoogleCloudOptions
        from apache_beam.options.pipeline_options import PipelineOptions
        from apache_beam.options.pipeline_options import StandardOptions
        from apache_beam.runners import DataflowRunner, DirectRunner
    ```



- Create a Pipeline[1] from PipelineOptions[2] object
    ```
        options = PipelineOptions()

        p = beam.Pipeline(options=options)
    ```

- Read in data into a PCollection[3]
    ```
        lines = p | "ReadLines" >> beam.io.ReadFromText("gs://path/to/input.txt")
    ```

- Run the pipeline using DirectRunner[5] or Cloud Dataflow [6]:
    ```
        cd $BASE_DIR
        # Set up environment variables
        export PROJECT_ID=$(gcloud config get-value project)
        # Run the pipeline
        python3 my_pipeline.py \
        --project=${PROJECT_ID} \
        --region=us-central1 \
        --stagingLocation=gs://$PROJECT_ID/staging/ \
        --tempLocation=gs://$PROJECT_ID/temp/ \
        --runner=DirectRunner
    ```

- Links
    - [1] https://beam.apache.org/releases/pydoc/2.28.0/apache_beam.pipeline.html
    - [2] https://beam.apache.org/releases/pydoc/2.28.0/apache_beam.options.pipeline_options.html
    - [3] https://beam.apache.org/releases/pydoc/2.28.0/apache_beam.pvalue.html
    - [4] https://beam.apache.org/releases/pydoc/2.28.0/apache_beam.io.textio.html#apache_beam.io.textio.ReadFromText
    - [5] https://beam.apache.org/documentation/runners/direct/
    - [6] https://beam.apache.org/documentation/runners/dataflow/
..

