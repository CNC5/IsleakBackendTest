import sqlalchemy.orm
import dataclasses
from typing import Optional


Base = sqlalchemy.orm.declarative_base()


class APIKey(Base):
    __tablename__ = 'api_keys'

    api_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'APIKey(api_key={self.api_key!r})'
