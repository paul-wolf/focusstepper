import os

import boto3

REGION_NAME = "eu-central-1"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

def aws_creds():
    return {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }

def get_resource_client(resource_name):
    """The preferred way to get an AWS resource client.

    For some reason, `boto3.resource()` does not work for some resources.

    """
    creds = aws_creds()
    session = boto3.session.Session(
        creds["aws_access_key_id"],
        creds["aws_secret_access_key"],
        region_name=REGION_NAME,
    )

    return session.client(resource_name)

def get_resource(resource_name):
    """The preferred way to get an AWS resource client.

    For some reason, `boto3.resource()` does not work for some resources.

    """
    creds = aws_creds()
    session = boto3.session.Session(
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        region_name=REGION_NAME,
    )

    return session.resource(resource_name)

def get_s3():
    config = boto3.session.Config(
        s3={"addressing_style": "path"}, signature_version="s3v4"
    )
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=config,
        region_name=REGION_NAME,
    )


def get_url(bucket, key):
    s3 = get_s3()
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key, "ContentType": "image/png"},
        ExpiresIn=600,
    )

def store_stream_s3(bucket_name, fp, key_name, replace=True):

    s3 = get_resource('s3')
    return s3.Object(bucket_name, key_name).put(Body=fp)
