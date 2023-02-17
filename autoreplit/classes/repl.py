from dataclasses import dataclass
from typing import Optional


@dataclass
class BasicRepl:
    """A basic repl dataclass."""

    id: str  #: The repl id
    url: str  #: The repl url
    title: Optional[str]  #: The repl title
