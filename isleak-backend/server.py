from flask_base import MainServer, request
from parser import parse_custom_query_into_kql, InvalidQueryException

app = MainServer(__name__)


@app.route('/search', methods=['GET'])
@app.require_api_key
def search():
    custom_query = request.json.get('query')
    try:
        kql_query = parse_custom_query_into_kql(custom_query=custom_query)
    except InvalidQueryException as e:
        return {'error': str(e), 'data': ''}, 400
    data = app.elasticsearch_connection.search(query=kql_query).body
    return {'error': '', 'data': data}, 200


@app.route('/ping', methods=['GET'])
def ping():
    return {'error': '', 'data': 'pong'}, 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
