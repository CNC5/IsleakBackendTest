import sqlalchemy.orm
import dataclasses
from typing import Optional


class Base(sqlalchemy.orm.DeclarativeBase):
    def as_dict(self):
        data_dict = {}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            data_dict.update({field.name: value})
        return data_dict


class APIKey(Base):
    __tablename__ = 'api_keys'

    api_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'APIKey(api_key={self.api_key!r})'
