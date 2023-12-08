import boto3
import os
import pytest
from moto import mock_s3

AWS_REGION = "us-west-1"
BUCKET_NAME = "test_web_assets_bucket"
API_BASE_URL = "https://www.test-api-url.com"
CACHE_DURATION = "60"


@pytest.fixture(autouse=True)
def set_aws_env():
    os.environ["AWS_REGION"] = AWS_REGION

    yield

    del os.environ["AWS_REGION"]


@pytest.fixture(autouse=True)
def set_mock_aws_lambda_env():
    os.environ["BUCKET_NAME"] = BUCKET_NAME
    os.environ["API_BASE_URL"] = API_BASE_URL
    os.environ["CACHE_DURATION"] = CACHE_DURATION

    yield

    del os.environ["BUCKET_NAME"]
    del os.environ["API_BASE_URL"]
    del os.environ["CACHE_DURATION"]


@pytest.fixture(autouse=True)
def create_mock_web_assets_bucket():
    with mock_s3():
        s3_client = boto3.client("s3", region_name=AWS_REGION)

        s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
        )

        s3 = boto3.resource("s3", region_name=AWS_REGION)

        for file_name in ["index.html", "bundle.js"]:
            obj = s3.Object(BUCKET_NAME, file_name)
            obj.put(Body=f"This is a dummy {file_name}")

        yield
