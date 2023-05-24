import pydantic
from abc import ABC
from typing import Optional, Generic, TypeVar, TypeAlias
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

class AllOptional(pydantic.main.ModelMetaclass):
    ## Fix pydantic w/ new system madness
    ## https://stackoverflow.com/questions/67699451/make-every-fields-as-optional-with-pydantic
    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)