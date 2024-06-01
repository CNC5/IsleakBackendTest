from flask_base import MainServer, request
from parser import parse_custom_query_into_kql

app = MainServer(__name__)


@app.route('/search', methods=['GET'])
@app.require_api_key
def search():
    custom_query = request.json.get('query')
    kql_query = parse_custom_query_into_kql(custom_query=custom_query)
    data = app.elasticsearch_connection.search(query=kql_query).body
    return {'error': '', 'data': data}


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
