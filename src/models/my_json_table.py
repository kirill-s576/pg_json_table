from pydantic import BaseModel, validator
from typing import List, Union
from src.database.postgres import (
    PostgresTable,
    PostgresSimpleQuery
)
from abc import ABC, abstractmethod


class JsonTableObjectInterface(ABC):
    """
    Basic interface for inserting data in MyJsonTable.
    Inherit from this interface and reimplement properties inside your object.
    """
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        pass

    @property
    @abstractmethod
    def items(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def body(self) -> Union[str, None]:
        pass

    @property
    @abstractmethod
    def author_id(self) -> str:
        pass

    @property
    @abstractmethod
    def author_name(self) -> str:
        pass

    @property
    @abstractmethod
    def created_date(self) -> str:
        pass

    @property
    @abstractmethod
    def created_time(self) -> str:
        pass

    @property
    @abstractmethod
    def updated_date(self) -> Union[str, None]:
        pass

    @property
    @abstractmethod
    def updated_time(self) -> Union[str, None]:
        pass

    @property
    @abstractmethod
    def counters_total(self) -> int:
        pass

    def dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "items":  self.items,
            "body":  self.body,
            "author_name":  self.author_name,
            "author_id":  self.author_id,
            "created_date":  self.created_date,
            "created_time":  self.created_time,
            "updated_date":  self.updated_date,
            "updated_time":  self.updated_time,
            "counters_total": self.counters_total,
        }


class MyJsonTableJsonFieldValidator(BaseModel):
    """
    Validator for MyJsonTable Json Field.
    """
    id: str
    path: str
    items: List[str] = []
    body: str = None
    author_name: str
    author_id: str
    created_date: str
    created_time: str
    updated_date: str = None
    updated_time: str = None
    counters_total: int

    # Uncomment below code if need extended validation for path field.
    # @validator('path')
    # def path_has_path_format(cls, value:str):
    #     if not value.startswith("http"):
    #         raise ValueError("must starts with 'http'")
    #     return value


class MyJsonTable(PostgresTable):

    json_field_validator:BaseModel = MyJsonTableJsonFieldValidator

    # Public methods

    def get_validated_json_object(self, json_data):
        """
        Returns serialized object.
        :param json_data:
        :return:
        """
        validated_object = self.json_field_validator(**json_data)
        return validated_object

    def insert_row(self, obj: JsonTableObjectInterface):
        """
        Insert new row in database
        :param kwargs: attributes for new row.
        :return:
        """
        validated_object = self.get_validated_json_object(obj.dict())
        json_string = validated_object.json()
        query_string = self._get_insert_row_query_string(json_string)
        query = PostgresSimpleQuery(
            query=query_string,
            bound_vars=None
        )
        with self.connection:
            cursor = self.connection.send_query(query)
        return cursor

    #Private methods

    def _get_create_table_query_string(self) -> str:
        """
        Returns SQL query for making table.
        """
        query_string = \
        f"""
        CREATE TABLE 
        IF NOT EXISTS {self.name}
        (id SERIAL PRIMARY KEY, 
        json jsonb)
        """
        return query_string

    def _get_insert_row_query_string(self, json_string: str):
        """
        Returns SQL query for inserting new row in table.
        :param json_string:
        """
        query_string = \
        f"""
        INSERT INTO {self.name}
        (json)
        VALUES
        ('{json_string}')
        """
        return query_string

    def _check_table(self):
        """
        Create table if not exists
        :return: Returns True if created else False.
        """
        query_string = self._get_create_table_query_string()
        query = PostgresSimpleQuery(
            query=query_string,
            bound_vars=None
        )
        with self.connection:
            self.connection.send_query(query)