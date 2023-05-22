from ..commonTyping import JsonType
from abc import ABCMeta
from typing import Optional


class ResultError(Exception):
    """Raised if result does not exist."""

    pass


class QueryResultBase(metaclass=ABCMeta):
    """The base object of :class:`.QueryResult`. It is also the base of all other result wrappers."""

    __slots__ = ()

    def __init__(self, opname: Optional[str], json: JsonType) -> None:
        if not opname is None:
            data = json["data"][opname]
        else:
            data = json
        if data is None:
            raise ResultError("Result does not exist.")
        key: str
        for key in self.__slots__:
            if key in data:
                self.__setattr__(key, data[key])
            else:
                self.__setattr__(key, None)

    def __str__(self) -> str:
        result = f"{self.__class__.__name__}("
        if len(self.__slots__) < 1:
            return result + ")"
        s: str
        for s in self.__slots__:
            result += f"{s}={getattr(self, s)}, "
        return result[:-2] + ")"


class QueryResult(QueryResultBase):
    """A un-slotted query result object for :meth:`autoreplit.ReplitClient.rawQuery`"""

    def __init__(self, opname: Optional[str], json: JsonType) -> None:
        # Tmp-fix, reduntant
        if not opname is None:
            data = json["data"][opname]
        else:
            data = json
        self.__slots__ = data.keys()
        super().__init__(opname, json)
