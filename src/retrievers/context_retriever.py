from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from data.fewshots import NEIGHBORHOOD_EXAMPLES
from data.prompts import TEXT_TO_CYPHER_PROMPT
from data.schemas import NEO4J_SCHEMA
from src.graph.neo4j_client import driver
from src.llms import llm, llm


# def neighborhood_formatter(record) -> RetrieverResultItem:
#     data = record.data()
#
#     entity_id   = data.get("entity_id", "")
#     entity_name = data.get("entity_name", "")
#     entity_type = data.get("entity_type", "")
#
#     parts = [f"## {entity_type}: {entity_name} ({entity_id})"]
#
#     # Campos opcionales según tipo de entidad
#     field_labels = {
#         "full_name":              "Full name",
#         "description":            "Description",
#         "symbol":                 "Symbol",
#         "ic":                     "Information Content",
#         "phenotypes":             "Phenotypes",
#         "gene_phenotypes":        "Gene phenotypes",
#         "disease_phenotypes":     "Disease phenotypes",
#         "diseases":               "Associated diseases",
#         "causal_genes":           "Causal genes",
#         "inheritance":            "Inheritance",
#         "variants":               "Variants",
#         "ancestors":              "HPO ancestors",
#         "children":               "HPO children",
#         "diseases_with_phenotype":"Diseases with this phenotype",
#     }
#
#     for field, label in field_labels.items():
#         value = data.get(field)
#         if not value:
#             continue
#         if isinstance(value, list):
#             clean = [v for v in value if v]
#             if clean:
#                 # Truncar descripción
#                 if field == "description" and len(str(clean[0])) > 300:
#                     parts.append(f"{label}: {str(clean[0])[:300]}...")
#                 else:
#                     parts.append(f"{label}: {', '.join(str(v) for v in clean)}")
#         elif value:
#             text = str(value)
#             if field == "description" and len(text) > 300:
#                 text = text[:300] + "..."
#             parts.append(f"{label}: {text}")
#
#     return RetrieverResultItem(
#         content="\n".join(parts),
#         metadata={"entity_id": entity_id, "entity_type": entity_type}
#     )

t2c_context_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,
    custom_prompt=TEXT_TO_CYPHER_PROMPT,
    neo4j_schema=NEO4J_SCHEMA,
    examples=NEIGHBORHOOD_EXAMPLES
    #result_formatter=neighborhood_formatter
)

if __name__ == '__main__':
    query_text="Which phenotypes of 'neurofibromatosis type 1' are not associated to 'chromosome 17q11.2 deletion syndrome, 1.4Mb'? Sort phenotypes by IC_disease"
    res = t2c_context_retriever.search(query_text=query_text)
    print(res.metadata['cypher'])