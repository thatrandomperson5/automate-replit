from dataclasses import dataclass
from typing import Optional
from typing import cast
from ..commonTyping import JsonType
from .queryResult import QueryResultBase


@dataclass
class SimpleUser:
    """A simple user object, provides username and id."""

    username: str
    id: str


@dataclass
class BasicRepl:
    """A basic repl dataclass."""

    id: str  #: The repl id
    url: str  #: The repl url
    title: Optional[str]  #: The repl title


class BasicComment(QueryResultBase):
    """A basic comment class."""

    id: str  #: Comment id
    repl: BasicRepl  #: Comment repl

    __slots__ = locals()["__annotations__"].keys()

    def __init__(self, json: JsonType) -> None:
        super().__init__(None, json)
        self.repl = BasicRepl(
            cast(JsonType, self.repl)["id"],
            cast(JsonType, self.repl)["url"],
            cast(JsonType, self.repl)["title"],
        )
