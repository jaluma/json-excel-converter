import json

from json_excel_api import api


def test_create_item():
    f = open('examples/request1.json')
    data = json.load(f)
    f.close()

    response = api.create_item(data)
    assert response is not None
