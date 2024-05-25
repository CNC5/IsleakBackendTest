from keygen import add_new_key
from database import OperatorAliases, APIKey
from elastic import client as elastic_client
import requests


def test_backend():
    api_key = add_new_key()
    database = OperatorAliases()
    elastic_client.index(index='news', document={'category': 'weather', 'contents': {'1': 'windy', '2': 'less windy'}})

    response = requests.request('POST', 'http://localhost:5000',
                                headers={'Content-Type': 'application/json'},
                                data={'api_key': api_key, 'query': 'less and windy'})
    assert response.status_code == 200
    database.delete_api_key(api_key)