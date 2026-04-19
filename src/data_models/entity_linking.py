from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LinkStrategy(str, Enum):
    EXACT = "exact"
    FULLTEXT = "fulltext"
    VECTOR = "vector"
    NONE = "none"

class Mention(BaseModel):
    text: str
    start: int
    end: int

class LinkedEntity(BaseModel):
    mention: str
    node_id: Optional[str]
    name: str
    label: str
    score: float
    strategy: LinkStrategy