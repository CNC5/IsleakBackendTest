from functools import wraps
from flask import Flask, request
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine
import sqlalchemy.orm
from sqlalchemy.engine import Engine
from elasticsearch import Elasticsearch
from config import DatabaseConfig, ElasticsearchConfig
from database import APIKey


class MainServer(Flask):
    database_engine: Engine
    database_session_factory: sqlalchemy.orm.sessionmaker[sqlalchemy.orm.Session]
    database_config: DatabaseConfig
    elasticsearch_connection: Elasticsearch
    elasticsearch_config: ElasticsearchConfig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.from_object(__name__)
        self.database_config = DatabaseConfig()
        self.elasticsearch_config = ElasticsearchConfig()
        self.database_engine = create_engine(
            f'postgresql+psycopg2://{self.database_config.db_user}:{self.database_config.db_pass}'
            f'@{self.database_config.db_host}:{self.database_config.db_port}/{self.database_config.db_name}',
            pool_size=256, pool_timeout=120, max_overflow=0, poolclass=QueuePool)
        self.database_session_factory = sqlalchemy.orm.sessionmaker(self.database_engine)
        self.elasticsearch_connection = Elasticsearch(
            f'https://{self.elasticsearch_config.elastic_host}:{self.elasticsearch_config.elastic_port}',
            verify_certs=False, ca_certs=self.elasticsearch_config.elastic_certificate_path,
            basic_auth=(self.elasticsearch_config.elastic_username, self.elasticsearch_config.elastic_password))
        APIKey.metadata.create_all(self.database_engine)

    # database_operator_instance.insert_rows([APIKey(key_name)])
    def insert_rows(self, data: list) -> bool:
        with self.database_session_factory() as database_session:
            database_session.add_all(data)
            database_session.commit()
        return True

    def query_row_by_primary_field(self, object_class, value):
        with self.database_session_factory() as database_session:
            row = database_session.get(object_class, value)
        return row

    def delete_row(self, object_class, object_class_column_filter) -> bool:
        with self.database_session_factory() as database_session:
            database_session.execute(
                sqlalchemy.delete(object_class)
                .where(object_class_column_filter))
            database_session.commit()
        return True

    def require_api_key(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.json.get('api_key')
            if not api_key or not self.query_row_by_primary_field(APIKey, api_key):
                return {'error': 'Unauthorized', 'data': ''}, 401
            return f(*args, **kwargs)
        return decorated_function
