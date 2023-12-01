def handler(event: dict, context) -> dict:
    return {"statusCode": 200}


def get_file_path(event: dict) -> str:
    if "proxy" in event["pathParameters"]:
        return event["pathParameters"]["proxy"]

    return "index.html"
