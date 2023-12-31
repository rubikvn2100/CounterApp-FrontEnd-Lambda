import json
from src.web_asset_fetcher.index import (
    handler,
    get_file_path,
    fetch_file,
    create_config_json_response,
    add_cache_control_headers,
)


def test_handler_config_json_case():
    event = {"pathParameters": {"proxy": "config.json"}}
    context = {}
    expected_response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Cache-Control": "max-age=60"},
        "body": json.dumps({"apiBaseUrl": "https://www.test-api-url.com"}),
    }

    response = handler(event, context)

    assert response == expected_response


def test_handler_general_case():
    event = {"pathParameters": {}}
    context = {}
    expected_response = {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html", "Cache-Control": "max-age=60"},
        "body": "This is a dummy index.html",
    }

    response = handler(event, context)

    assert response == expected_response


def test_get_file_path_with_proxy():
    event = {"pathParameters": {"proxy": "dummy_file_path"}}

    file_path = get_file_path(event)

    assert file_path == "dummy_file_path"


def test_get_file_path_without_proxy():
    event = {"pathParameters": {}}

    file_path = get_file_path(event)

    assert file_path == "index.html"


def test_create_config_json_response():
    expected_response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"apiBaseUrl": "https://www.test-api-url.com"}),
    }

    response = create_config_json_response()

    assert response == expected_response


def test_fetch_file_file_not_found():
    file_path = "non_exist_file"
    expected_response = {"statusCode": 404, "body": "File not found"}

    response = fetch_file(file_path)

    assert response == expected_response


def test_fetch_file_index_html():
    file_path = "index.html"
    expected_response = {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": "This is a dummy index.html",
    }

    response = fetch_file(file_path)

    assert response == expected_response


def test_add_cache_control_headers_with_headers():
    input_response = {"headers": {"Dummy-Header": "DummyValue"}}
    expected_output_response = {
        "headers": {"Dummy-Header": "DummyValue", "Cache-Control": "max-age=60"}
    }

    output_response = add_cache_control_headers(input_response)

    assert output_response == expected_output_response


def test_add_cache_control_headers_without_headers():
    input_response = {}
    expected_output_response = {"headers": {"Cache-Control": "max-age=60"}}

    output_response = add_cache_control_headers(input_response)

    assert output_response == expected_output_response
