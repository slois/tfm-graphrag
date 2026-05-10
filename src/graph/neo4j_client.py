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

index_map = {
    'phenotype': ("phenotypic_feature_index", None, "biolink:PhenotypicFeature"),# "phenotypic_feature_fulltext_index"
    'disease': ("disease_index", None, "biolink:Disease"),  # "disease_fulltext_index"
    'gene': ("gene_index", None, "biolink:Gene"),
}

if __name__ == "__main__":
    from neo4j_graphrag.schema import get_schema
    print(get_schema(driver, sanitize=True))