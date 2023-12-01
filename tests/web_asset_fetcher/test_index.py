from src.web_asset_fetcher.index import handler


def test_handler():
    event = {}
    context = {}
    expected_response = {"statusCode": 200}

    response = handler(event, context)

    assert response == expected_response
