from database import OperatorAliases, APIKey
import secrets

def create_new_key():
    database = OperatorAliases()
    new_key = secrets.token_urlsafe(64)
    database.insert_rows([APIKey(api_key=new_key)])
    return new_key
