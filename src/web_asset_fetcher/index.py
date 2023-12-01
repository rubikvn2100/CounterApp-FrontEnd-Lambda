import boto3
import json
import mimetypes
import os


def handler(event: dict, context) -> dict:
    file_path = get_file_path(event)

    print(f'Resolved file path: "{file_path}"')

    if file_path == "config.json":
        return create_config_json_response()

    return fetch_file(file_path)


def get_file_path(event: dict) -> str:
    if "proxy" in event["pathParameters"]:
        return event["pathParameters"]["proxy"]

    return "index.html"


def create_config_json_response():
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"apiBaseUrl": os.environ["API_BASE_URL"]}),
    }


def fetch_file(file_path: str) -> dict:
    s3 = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]

    try:
        s3_response = s3.get_object(Bucket=bucket_name, Key=file_path)
    except Exception as e:
        print(f"S3 retrieval error: {e}")

        return {"statusCode": 404, "body": "File not found"}

    mime_type, _ = mimetypes.guess_type(file_path)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": mime_type},
        "body": s3_response["Body"].read().decode("utf-8"),
    }
