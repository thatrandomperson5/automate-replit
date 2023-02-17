from .queryResult import QueryResultBase
from typing import cast
from ..commonTyping import JsonType
from .repl import BasicRepl


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
