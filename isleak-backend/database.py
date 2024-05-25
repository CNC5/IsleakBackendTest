import dataclasses
import logging
import socket
import time
import typing
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from config import DatabaseConfig


def wait_for_database_up() -> None:
    config = DatabaseConfig()
    database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    total_seconds_awaited = 0
    timeout = 180
    while True:
        try:
            database_socket.connect((config.db_host, config.db_port))
            database_socket.close()
            break
        except socket.error:
            if total_seconds_awaited > timeout:
                raise Exception(f'Database is not up after {total_seconds_awaited}s')
            time.sleep(0.5)
            total_seconds_awaited += 0.5


logger = logging.getLogger(__name__)


class Base(sqlalchemy.orm.DeclarativeBase):
    def as_dict(self):
        data_dict = {}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            data_dict.update({field.name: value})
        return data_dict


@dataclasses.dataclass
class APIKey(Base):
    __tablename__ = 'api_keys'

    api_key: Mapped[Optional[str]] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'APIKey(api_key={self.api_key!r})'


database_types_union = typing.Union[type(APIKey)]


class DatabaseConnector(DatabaseConfig):
    def __init__(self):
        super().__init__()
        self.engine = sqlalchemy.create_engine(f'postgresql+psycopg2://'
                                               f'{self.db_user}:{self.db_pass}'
                                               f'@{self.db_host}:{self.db_port}/'
                                               f'{self.db_name}')


class DatabaseOperator:
    def __init__(self):
        self.engine = DatabaseConnector().engine
        Base.metadata.create_all(self.engine)

    # database_operator_instance.insert_rows([APIKey(key_name)])
    def insert_rows(self, data: list) -> bool:
        with sqlalchemy.orm.Session(self.engine) as database_session:
            database_session.add_all(data)
            database_session.commit()
        return True

    def query_row_by_primary_field(self, object_class: database_types_union, value):
        with sqlalchemy.orm.Session(self.engine) as database_session:
            row = database_session.get(object_class, value)
        return row

    def delete_row(self, object_class: database_types_union, object_class_column_filter) -> bool:
        with sqlalchemy.orm.Session(self.engine) as database_session:
            database_session.execute(
                sqlalchemy.delete(object_class)
                .where(object_class_column_filter))
            database_session.commit()
        return True


class OperatorAliases(DatabaseOperator):
    def __init__(self):
        super().__init__()

    # API Keys
    def add_api_key(self, **kwvalues) -> bool:
        return self.insert_rows([APIKey(**kwvalues)])

    def get_api_key(self, key_name: str):
        return self.query_row_by_primary_field(APIKey, key_name)

    def delete_api_key(self, key_name: str) -> bool:
        return self.delete_row(key_name, APIKey, APIKey.api_key == key_name)


wait_for_database_up()
