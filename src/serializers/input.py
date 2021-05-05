import pydantic
import datetime
from typing import List, Union
from src.models.my_json_table import JsonTableObjectInterface


class MarkSerializer(pydantic.BaseModel):
    """

    """
    text: str


class ContentSerializer(pydantic.BaseModel):
    """

    """
    marks: List[MarkSerializer]
    description: str


class CountersSerializer(pydantic.BaseModel):
    """

    """
    score: int
    mistakes: int

class AuthorSerializer(pydantic.BaseModel):
    """

    """
    id: str
    username: str


class InputJsonSerializer(pydantic.BaseModel):
    """

    """
    id: str
    address: str
    type: str
    author: AuthorSerializer
    content: ContentSerializer
    counters: CountersSerializer
    updated: datetime.datetime
    created: datetime.datetime


class InputJsonDatabaseConnector(JsonTableObjectInterface):

    def __init__(self, validated_object: InputJsonSerializer):
        self.validated_object = validated_object

    @property
    def id(self) -> str:
        return self.validated_object.id

    @property
    def path(self) -> str:
        return self.validated_object.address

    @property
    def items(self) -> List[str]:
        items = [
            mark.text for mark in self.validated_object.content.marks
        ]
        return items

    @property
    def body(self) -> Union[str, None]:
        return self.validated_object.content.description

    @property
    def author_id(self) -> str:
        return self.validated_object.author.id

    @property
    def author_name(self) -> str:
        return self.validated_object.author.username

    @property
    def created_date(self) -> str:
        created_date_string = self.validated_object.created.strftime("%Y-%m-%d")
        return created_date_string

    @property
    def created_time(self) -> str:
        created_time_string = self.validated_object.created.strftime("%H:%M:%S")
        return created_time_string

    @property
    def updated_date(self) -> Union[str, None]:
        if not self.validated_object.updated:
            return None
        updated_time_string = self.validated_object.updated.strftime("%H:%M:%S")
        return updated_time_string

    @property
    def updated_time(self) -> Union[str, None]:
        if not self.validated_object.updated:
            return None
        updated_time_string = self.validated_object.updated.strftime("%H:%M:%S")
        return updated_time_string

    @property
    def counters_total(self) -> int:
        return self.validated_object.counters.score + self.validated_object.counters.mistakes
