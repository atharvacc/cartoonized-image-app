
import numpy as np
import boto3
from PIL import Image
import os
from datetime import datetime
import io
import json


def get_aws_creds():
    return (os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_ACCESS_KEY'])


def get_s3_client():
    aws_key, secret_key = get_aws_creds()
    s3_client = boto3.client(
        's3', aws_access_key_id=aws_key, aws_secret_access_key=secret_key
    )
    return s3_client


def get_sagemaker_runtime():
    aws_key, secret_key = get_aws_creds()
    region = os.environ['AWS_REGION']
    runtime = boto3.client(
        'runtime.sagemaker', region_name=region, aws_access_key_id=aws_key,
        aws_secret_access_key=secret_key
    )
    return runtime


def predict(img, bucket, endpoint_name):
    s3_client = get_s3_client()
    runtime = get_sagemaker_runtime()

    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format=img.format)
    in_mem_file.seek(0)
    file_name = datetime.strftime(
        datetime.now(), format="%m-%d-%Y-%H:%M:%S.jpg"
    )
    body = '{{"url": "https://{0}.s3.amazonaws.com/{1}"}}'.format(
        bucket, file_name)
    up = s3_client.upload_fileobj(
        in_mem_file, Bucket=bucket, Key=file_name, ExtraArgs={
            "ACL": "public-read"}
    )
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=body,
        ContentType="application/json")
    out = response['Body']
    pred = out.read()
    pred = np.array(json.loads(pred))
    pred = Image.fromarray(np.uint8(pred*255)).convert('RGB')
    return pred
