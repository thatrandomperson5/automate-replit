# New, efficent format

from graphql_query import Operation, Query, Field
from typing import List, Union
from .utils import ExtendableBase, AllOptional




class FieldBase(Field, ExtendableBase, metaclass=AllOptional):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.results = {}

    def multiple(self, *children: List[Union["FieldBase", str]]) -> None:
        self.fields = children
        for child in children:
            if type(child) != str:
                continue
            self.results[child] = self.__annotations__[child]


class QueryBase(Query, ExtendableBase, metaclass=AllOptional):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.results = {}

    def multiple(self, *children: List[Union["FieldBase", str]]) -> None:
        self.fields = children
        for child in children:
            if type(child) != str:
                continue
            self.results[child] = self.__annotations__[child]


class OperationBase(Operation, ExtendableBase, metaclass=AllOptional):

        
    def multiple(self, *children: List[QueryBase]) -> None:
        self.queries = children
