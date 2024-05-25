from pyparsing import nestedExpr, ParseException
allowed_letters_set = set([letter for letter in 'qwertyuiopasdfghjklzxcvbnm ()'])


def recursively_assemble_kql_query(query_data: list | str) -> dict:
    if type(query_data) == str:
        return {"simple_query_string": {"query": query_data}}
    if query_data[0] == 'and':
        return {'bool': {'must':
                             [recursively_assemble_kql_query(query_data[1]),
                              recursively_assemble_kql_query(query_data[2])]
                         }}
    if query_data[0] == 'or':
        return {'bool': {'should':
                             [recursively_assemble_kql_query(query_data[1]),
                              recursively_assemble_kql_query(query_data[2])]
                         }}
    raise Exception('Invalid query')


def recursively_disassemble_custom_query(query_data: list | str):
    if type(query_data) == str:
        return query_data
    if len(query_data) != 3:
        raise Exception('Invalid query')
    if query_data[1].lower() == 'and':
        return ['and',
                recursively_disassemble_custom_query(query_data[0]),
                recursively_disassemble_custom_query(query_data[2])]
    if query_data[1].lower() == 'or':
        return ['or',
                recursively_disassemble_custom_query(query_data[0]),
                recursively_disassemble_custom_query(query_data[2])]
    raise Exception('Invalid query')


def parse_custom_query_into_kql(custom_query: str):
    if not is_valid_custom_query(custom_query):
        Exception('Invalid query')
    custom_query = f'({custom_query})'
    try:
        query_data = nestedExpr('(', ')').parseString(custom_query).asList()
    except ParseException:
        raise Exception('Invalid query')
    while len(query_data) == 1:
        query_data = query_data[0]
    try:
        query_data = recursively_disassemble_custom_query(query_data)
    except:
        raise Exception('Invalid query')
    return recursively_assemble_kql_query(query_data)


def is_valid_custom_query(custom_query: str):
    if custom_query.count('(') == custom_query.count(')'):
        return False
    if not set([letter for letter in custom_query.lower()]).issubset(allowed_letters_set):
        return False
    return True
