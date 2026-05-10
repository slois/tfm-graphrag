from enum import Enum
from typing import Optional, Literal, List, Union, Annotated

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: Optional[str] = Field(description="Unique identifier (in case of be identified in query text)")
    mention: str = Field(description="Free-text mention identified as entity in query text")

class SeverityType(str, Enum):
    Mild = "mild"
    Moderate = "Moderate"
    Severe = "Severe"
    Unknown = "Unknown"

class Phenotype(Entity):
    id: Optional[str] = Field(description="HGNC identifier", pattern=r"[HM]P:[0-9]{7}")
    type: Literal['biolink:PhenotypicFeature'] = 'biolink:PhenotypicFeature'
    negated: bool = Field(description='Whether the phenotype is negated in the text')
    severity: Optional[SeverityType] = Field(description='Degree of severity of the phenotype', default=SeverityType.Unknown)

class Gene(Entity):
    id: Optional[str] = Field(description="HGNC identifier", pattern=r"HGNC:[0-9]*")
    type: Literal['biolink:Gene'] = 'biolink:Gene'
    full_name: Optional[str] = Field(description="Full name of the gene (not extract from original text)")

class Disease(Entity):
    type: Literal['biolink:Disease'] = 'biolink:Disease'

class QueryExtraction(BaseModel):
    phenotype: List[Phenotype]
    gene: List[Gene]
    disease: List[Disease]

    def __iter__(self):
        yield from self.gene
        yield from self.disease
        yield from self.phenotype