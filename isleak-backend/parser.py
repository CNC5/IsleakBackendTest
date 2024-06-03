from pyparsing import nestedExpr, ParseException

allowed_letters_set = set([letter for letter in 'qwertyuiopasdfghjklzxcvbnm ()'])


class InvalidQueryException(Exception):
    pass


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


def _readable_unwrap(data: list[list | str]):
    if type(data) == list[str]:
        return " ".join(data)
    elif type(data) == str:
        return data
    else:
        return f'({" ".join([_readable_unwrap(item) for item in data])})'


def recursively_disassemble_custom_query(query_data: list | str) -> list[list | str]:
    if type(query_data) == str:
        return query_data
    if len(query_data) != 3:
        raise InvalidQueryException(f'Query \'{_readable_unwrap(query_data)}\' '
                                    f'is {"more" if len(query_data) > 3 else "less"} than 3 key tokens')
    if query_data[1].lower() == 'and':
        return ['and',
                recursively_disassemble_custom_query(query_data[0]),
                recursively_disassemble_custom_query(query_data[2])]
    if query_data[1].lower() == 'or':
        return ['or',
                recursively_disassemble_custom_query(query_data[0]),
                recursively_disassemble_custom_query(query_data[2])]
    raise InvalidQueryException(f'Query \'{_readable_unwrap(query_data)}\' '
                                f'does not contain OR/AND statement between keywords')


def parse_custom_query_into_kql(custom_query: str):
    if not is_valid_custom_query(custom_query):
        InvalidQueryException(f'Query \'{custom_query}\' contains invalid characters')
    parenthesised_custom_query = f'({custom_query})'
    try:
        query_data = nestedExpr('(', ')').parseString(parenthesised_custom_query).asList()
    except ParseException:
        raise InvalidQueryException(f'Query \'{custom_query}\' contains invalid parenthesis structure')
    while len(query_data) == 1:
        query_data = query_data[0]
    query_data = recursively_disassemble_custom_query(query_data)
    return recursively_assemble_kql_query(query_data)


def is_valid_custom_query(custom_query: str):
    if custom_query.count('(') == custom_query.count(')'):
        return False
    if not set([letter for letter in custom_query.lower()]).issubset(allowed_letters_set):
        return False
    return True
