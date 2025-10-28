from botocore.config import Config
import boto3

from app.core.config import AppConfig

s3_client = None
bucket: str = ""
seven_days_sec = 604800


def setup_s3(conf: AppConfig):
    global s3_client, bucket
    s3_client = boto3.client(
        "s3",
        region_name=conf.aws_region,
        aws_access_key_id=conf.aws_access_key_id,
        aws_secret_access_key=conf.aws_secret_access_key,
        endpoint_url=f'https://s3.{conf.aws_region}.amazonaws.com'

    )
    bucket = conf.aws_s3_bucket_name


def upload_file(file, key: str) -> any:
    return s3_client.upload_fileobj(file, bucket, key)


def create_presigned_url(key, expiration_sec=seven_days_sec):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration_sec,
    )
