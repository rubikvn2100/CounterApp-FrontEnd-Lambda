import boto3
import os
import pytest

AWS_REGION = "us-west-1"
BUCKET_NAME = "test_web_assets_bucket"


@pytest.fixture(autouse=True)
def set_aws_env():
    os.environ["AWS_REGION"] = AWS_REGION

    yield

    del os.environ["AWS_REGION"]


@pytest.fixture(autouse=True)
def set_mock_aws_lambda_env():
    os.environ["BUCKET_NAME"] = BUCKET_NAME

    yield

    del os.environ["BUCKET_NAME"]
