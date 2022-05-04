# batch_user_traffic_pipeline.py
'''
# Run Command:
python batch_user_traffic_pipeline.py --runner=DirectRunner \
    --input_path=events.json --output_path=out.json
'''

import argparse
import json
import typing
import apache_beam as beam
from apache_beam.transforms.combiners import CountCombineFn
from apache_beam.transforms.combiners import Count
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions

class CommonLog (typing.NamedTuple):
    ip           : str
    user_id      : str
    lat          : float
    lng          : float
    timestamp    : str
    http_request : str
    http_response: int
    num_bytes    : int
    user_agent   : str

class PerUserAggregation(typing.NamedTuple):
    user_id    : str
    page_views : int
    total_bytes: int
    max_bytes  : int
    min_bytes  : int

# String -> CommonLog
def parse_json(s):
    row = json.loads(s)
    return CommonLog(**row)

def run():
    # Command line arguments
    parser = argparse.ArgumentParser(description='Load from Json into BigQuery')
    # parser.add_argument('--project',required=True, help='Specify Google Cloud project')
    # parser.add_argument('--region', required=True, help='Specify Google Cloud region')
    # parser.add_argument('--staging_location', required=True, help='Specify Cloud Storage bucket for staging')
    # parser.add_argument('--temp_location', required=True, help='Specify Cloud Storage bucket for temp')
    parser.add_argument('--runner', required=True, help='Specify Apache Beam Runner')
    parser.add_argument('--input_path', required=True, help='Path to events.json')
    parser.add_argument('--output_path', required=True, help='Path to output.txt')
    # parser.add_argument('--table_name', required=True, help='BigQuery table name')

    opts = parser.parse_args()

    # Setup Beam pipeline options
    # - Two types of options: GoogleCloudOptions and StandardOptions
    options = PipelineOptions(save_main_session=True)
    options.view_as(StandardOptions).runner              = opts.runner

    # Create the pipeline
    p = beam.Pipeline(options=options)

    input_path   = opts.input_path
    output_path  = opts.output_path
    # output_table = opts.table_name

    # Define pipeline componnents
    ( p | 'ReadFromFile' >> beam.io.ReadFromText(input_path)
          # None -> String

        | 'ParseJson' >> beam.Map(parse_json).with_output_types(CommonLog)
          # String -> CommonLog

        | 'PerUserAggregations' >> beam.GroupBy('user_id')
            .aggregate_field('user_id', CountCombineFn(), 'page_views')
            .aggregate_field('num_bytes', sum, 'total_bytes')
            .aggregate_field('num_bytes', max, 'max_bytes')
            .aggregate_field('num_bytes', min, 'min_bytes')
            .with_output_types(PerUserAggregation)
          # CommonLog -> PerUserAggregations

        | 'ToDict' >> beam.Map(lambda e: e._asdict())
          # PerUserAggregations -> dict

        | 'WriteToFile' >> beam.io.WriteToText(output_path)
          # dict -> None
    )
    p.run()

    print("Done");


if __name__ == '__main__':
    run()

