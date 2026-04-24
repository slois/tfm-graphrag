import os

from enum import Enum
from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv(override=False)

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI"),
    auth=(os.environ.get("NEO4J_USERNAME"), os.environ.get("NEO4J_PASSWORD")),
    notifications_min_severity="OFF", database=os.environ.get("NEO4J_DATABASE")
)

class EntityType (str, Enum):
    PHENOTYPE = "phenotype"
    DISEASE = "disease"
    GENE = "gene"

index_map = {
    EntityType.PHENOTYPE: ("phenotypic_feature_index", None, "biolink:PhenotypicFeature"),
    # "phenotypic_feature_fulltext_index"
    EntityType.DISEASE: ("disease_index", None, "biolink:Disease"),  # "disease_fulltext_index"
    EntityType.GENE: ("gene_index", None, "biolink:Gene"),
}

if __name__ == "__main__":
    from neo4j_graphrag.schema import get_schema
    print(get_schema(driver, sanitize=True))