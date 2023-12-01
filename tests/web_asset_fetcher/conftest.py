import boto3
import os
import pytest

AWS_REGION = "us-west-1"


@pytest.fixture(autouse=True)
def set_aws_env():
    os.environ["AWS_REGION"] = AWS_REGION

    yield

    del os.environ["AWS_REGION"]
