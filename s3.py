import os

import boto3

from dotenv import load_dotenv

load_dotenv()
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
    creds = aws_creds()
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


def get_matching_s3_objects(s3, bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """

    kwargs = {"Bucket": bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs["Prefix"] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp["Contents"]
        except KeyError:
            return

        for obj in contents:
            key = obj["Key"]
            if key.startswith(prefix) and key.endswith(suffix):
                yield obj

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs["ContinuationToken"] = resp["NextContinuationToken"]
        except KeyError:
            break


def get_matching_s3_keys(s3, bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(s3, bucket, prefix, suffix):
        yield obj["Key"]

def get_object_to_file(bucket_name, key_name, path):
    """Gets a file and writes it to the local file system in path."""
    s3 = get_resource("s3")
    return s3.Bucket(bucket_name).download_file(key_name, path)
