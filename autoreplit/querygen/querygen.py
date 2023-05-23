# New, efficent format

from graphql_query import Operation, Query, Field
from abc import ABC
from typing import List, Optional, Generic, TypeVar, Union, TypeAlias
from .commonTyping import JsonType
from types import MappingProxyType

class ResultObject(MappingProxyType):
    def __init__(self, data: JsonType):
        pass
        

class CallbackInit:
    __slots__ = ("cb", "typ")

    def __init__(self, cb: callable, typ: type) -> None:
        self.cb = cb
        self.typ = typ

    def __call__(self, *args, **kwargs):
        self.cb(self.typ(*args, **kwargs))


T = TypeVar("T")
TypedField: TypeAlias = Generic[T] #: Signifies result type



class ExtendableBase(ABC):
    def __getattr__(self, name: str) -> Optional[type]:
        if not name in self.__annotations__:
            raise ValueError(f'Invalid query option "{name}"')
        elif self.__annotations__[name] in {TypedField[T], str, int, bool}:
            self.multiple(name)

        elif hasattr(self.__annotations__[name], "needsArguments"):
            return CallbackInit(self.multiple, self.__annotations__[name])
        else:
            instance = self.__annotations__[name]()
            self.multiple(instance)  # Create a instance of the type
            return instance


class FieldBase(Field, ExtendableBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.results = {}

    def multiple(self, *children: List[Union["FieldBase", str]]) -> None:
        self.fields = children
        for child in children:
            if type(child) != str:
                continue
            self.results[child] = self.__annotations__[child]


class QueryBase(Query, ExtendableBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.results = {}

    def multiple(self, *children: List[Union["FieldBase", str]]) -> None:
        self.fields = children
        for child in children:
            if type(child) != str:
                continue
            self.results[child] = self.__annotations__[child]


class OperationBase(Operation, ExtendableBase):

        
    def multiple(self, *children: List[QueryBase]) -> None:
        self.queries = children
