from src.web_asset_fetcher.index import handler, get_file_path, fetch_file


def test_handler():
    event = {}
    context = {}
    expected_response = {"statusCode": 200}

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
