# batch_minute_traffic_pipeline.py
import argparse
import typing
import json
from datetime import datetime
import apache_beam as beam
from apache_beam.transforms.combiners import CountCombineFn
from apache_beam.options.pipeline_options import PipelineOptions

def parse_json(s):
    row = json.loads(s)
    return CommonLog(**row)

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

def add_timestamp(e):
    # datetime.strptime("2021-06-18T14:32:29.305371Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    ts = datetime.strptime(e.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    return beam.window.TimestampedValue(e, ts)

class GetTimestampFn(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        window_start = window.start.micros
        output = {'page_views': element, 'timestamp': window_start}
        yield output

def run():
    # Setup the argument parser
    parser = argparse.ArgumentParser(description='Aggregate Metrics by Fixed Windows')
    parser.add_argument('--input_path',required=True,help='Input file')
    parser.add_argument('--output_path',required=True,help='Output file')

    # Parse arguments and store as options
    opts = parser.parse_args()

    input_path = opts.input_path
    output_path = opts.output_path

    # Use the options
    options = PipelineOptions(save_main_session=True)
    # options.view_as(StandardOptions).runner = 'DirectRunner'

    p = beam.Pipeline(options=options)

    ( p | "ReadFromFile" >> beam.io.ReadFromText(input_path)
        # None -> String

        | "ParseJson" >> beam.Map(parse_json).with_output_types(CommonLog)
          # String -> CommonLog

        | "AddTimestamp" >> beam.Map(add_timestamp)
          # CommonLog -> CommonLog    # Type unchanged

        | "WindowByMinute" >> beam.WindowInto(beam.window.FixedWindows(1*60))
          # CommonLog -> CommonLog    # Type unchanged

        | "CountPerMinute" >> beam.CombineGlobally(CountCombineFn()).without_defaults()

        | "AddWindowTimestamp" >> beam.ParDo(GetTimestampFn())

        # | "CheckType" >> beam.Map(lambda x: type(x))

        | "WriteToFile" >> beam.io.WriteToText(output_path)
        # String -> None
    )

    p.run()

    print("Done!")

if __name__ == '__main__':
    run()
