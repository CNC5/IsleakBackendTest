from flask import Flask, request, jsonify
import logging
from database import OperatorAliases
from elastic import client as elastic_client
from parser import parse_custom_query_into_kql

logger = logging.getLogger(__name__)
app = Flask(__name__)
database = OperatorAliases()


@app.route('/search', methods=['POST'])
def search():
    api_key = request.json['api_key']
    custom_query = request.json['query']
    if not api_key:
        return {'error': 'Unauthorized', 'data': ''}, 401
    if not database.get_api_key(api_key):
        return {'error': 'Unauthorized', 'data': ''}, 401
    try:
        parsed_query = parse_custom_query_into_kql(custom_query)
    except:
        return {'error': 'Invalid query', 'data': ''}, 400
    data = elastic_client.search(query=parsed_query).body
    return {'error': '', 'data': data}, 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
