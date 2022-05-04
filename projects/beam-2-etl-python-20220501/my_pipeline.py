# my_pipeline.py
# - Working version
import argparse
import time
import logging
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.runners import DataflowRunner, DirectRunner
from apache_beam.io.textio import ReadFromText

# ### functions and classes

# TODO: Add parse_json function

# ### main

def run():

    # Command line arguments
    parser = argparse.ArgumentParser(description='Convert Json into BigQuery using Schemas')
    parser.add_argument('--project',required=True, help='Specify Google Cloud project')
    parser.add_argument('--region', required=True, help='Specify Google Cloud region')
    parser.add_argument('--stagingLocation', required=True, help='Specify Cloud Storage bucket for staging')
    parser.add_argument('--tempLocation', required=True, help='Specify Cloud Storage bucket for temp')
    parser.add_argument('--runner', required=True, help='Specify Apache Beam Runner')

    opts = parser.parse_args()

    # Setting up the Beam pipeline options
    options = PipelineOptions()
    options.view_as(GoogleCloudOptions).project = opts.project
    options.view_as(GoogleCloudOptions).region = opts.region
    options.view_as(GoogleCloudOptions).staging_location = opts.stagingLocation
    options.view_as(GoogleCloudOptions).temp_location = opts.tempLocation
    options.view_as(GoogleCloudOptions).job_name = '{0}{1}'.format('my-pipeline-',time.time_ns())
    options.view_as(StandardOptions).runner = opts.runner

    # Add static input and output strings
    input_file = "gs://qwiklabs-gcp-04-1af931ded40a/events.json"

    # Table schema for BigQuery
    table_schema = 'ip:STRING,user_id:STRING,lat:STRING,lng:STRING,timestamp:STRING,' + 'http_request:STRING,http_response:INTEGER,num_bytes:INTEGER,user_agent:STRING'

    # Create the pipeline
    p = beam.Pipeline(options=options)

    '''
    Steps:
    1) Read something
    2) Transform something
    3) Write something
    '''

    # Add transformation steps to pipeline
    p | "ReadLines" >> beam.io.ReadFromText(input_file) \
      | "ParseLines" >> beam.Map(lambda str: json.loads(str)) \
      | "WriteToBQ" >> beam.io.WriteToBigQuery('logs','logs','qwiklabs-gcp-04-1af931ded40a',table_schema)

    logging.getLogger().setLevel(logging.INFO)
    logging.info("Building pipeline ...")

    p.run()

if __name__ == '__main__':
  run()
