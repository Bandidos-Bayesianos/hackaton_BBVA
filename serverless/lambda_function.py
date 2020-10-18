import json
import csv
import boto3
import base64
import botocore.response
s3client = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement
    queryStringParameters = event.get('queryStringParameters', None)
    offset = 0
    rows = 100
    lambdaFunc = 0
    fieldnames = None
    if (queryStringParameters != None):
        offset = int(queryStringParameters.get('offset', offset))
        rows = int(queryStringParameters.get('rows', rows))
        lambdaFunc = int(queryStringParameters.get('lambdaFunc', lambdaFunc))
        fieldnames = queryStringParameters.get('fieldnames', fieldnames)
    else:
        offset = int(event.get('offset', offset))
        rows = int(event.get('rows', rows))
        lambdaFunc = int(event.get('lambdaFunc', lambdaFunc))
        fieldnames = event.get('fieldnames', fieldnames)

    bucket_name = 'bbva-hack-2020'
    object_key = 'moriarty.csv'
    s3_resource = boto3.resource('s3')
    s3_object = s3_resource.Object(
        bucket_name=bucket_name, key=object_key
    )
    lines = get_object_bodylines(s3_object, offset)
    csv_reader = csv.DictReader(lines.iter_lines(), fieldnames=fieldnames)
    body = ""
    for x in range(rows):
        row = next(csv_reader)
        body = body+",".join(row)+"\n"

    fieldnames = fieldnames or csv_reader.fieldnames
    s3_path = "hola"+str(lambdaFunc)+".csv"
    s3_resource.Bucket(bucket_name).put_object(
        Key=s3_path, Body=body, ACL='public-read')

    new_offset = offset + lines.offset
    if new_offset < s3_object.content_length and lambdaFunc < 1:
        new_event = {
            **event,
            "offset": new_offset,
            "lambdaFunc": lambdaFunc+1,
            "fieldnames": fieldnames
        }
        invoke_lambda(context.function_name, new_event)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/json',
        },
        'body': "[]"
    }


def get_object_bodylines(s3_object, offset):
    resp = s3_object.get(Range=f'bytes={offset}-')
    body: botocore.response.StreamingBody = resp['Body']
    return BodyLines(body)


def invoke_lambda(function_name, event):
    payload = json.dumps(event).encode('utf-8')
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=payload
    )


class BodyLines:
    def __init__(self, body: botocore.response.StreamingBody, initial_offset=0):
        self.body = body
        self.offset = initial_offset

    def iter_lines(self, chunk_size=1024):
        """Return an iterator to yield lines from the raw stream.
        This is achieved by reading chunk of bytes (of size chunk_size) at a
        time from the raw stream, and then yielding lines from there.
        """
        pending = b''
        for chunk in self.body.iter_chunks(chunk_size):
            lines = (pending + chunk).splitlines(True)
            for line in lines[:-1]:
                self.offset += len(line)
                yield line.decode('utf-8')
            pending = lines[-1]
        if pending:
            self.offset += len(pending)
            yield pending.decode('utf-8')
