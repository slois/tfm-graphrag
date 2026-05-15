from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from data.fewshots import MULTIHOP_EXAMPLES
from data.prompts import MULTIHOP_PROMPT
from data.schemas import NEO4J_SCHEMA
from src.graph.neo4j_client import driver
from src.llms import llm


def multihop_formatter(record) -> RetrieverResultItem:
    """
    Formatea resultados de queries multi-hop en texto estructurado.
    Maneja dinámicamente cualquier combinación de columnas.
    """
    data = record.data()

    return RetrieverResultItem(
        content=str(record),
        metadata={"raw": data}
    )


# ── Retriever ──────────────────────────────────────────────────────────────────
multihop_t2c_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,
    neo4j_schema=NEO4J_SCHEMA,
    custom_prompt=MULTIHOP_PROMPT,
    examples=MULTIHOP_EXAMPLES,
    neo4j_database="dimonarchkg",
    result_formatter=multihop_formatter
)

if __name__ == "__main__":

    QUERY_TEXT="Which phenotypes are associated with diseases caused by gene HGNC:3942?"
    QUERY_TEXT="Which genes are associated with phenotypes linked to disease MONDO:0008796?"
    QUERY_TEXT="Which genes participate in biological pathways Reactome:R-HSA-3214841 and are associated with diseases presenting the phenotype HP:0002119?"
    QUERY_TEXT="Which genes are associated with diseases linked to variant CLINVAR:207024?"
    QUERY_TEXT="Which diseases are modeled by mouse genotypes that share phenotypes with the mouse ortholog of the gene HGNC:4065?"
    QUERY_TEXT="Which diseases involve pathway Reactome:R-HSA-1445148 and have phenotype HP:0000040?"

    result = multihop_t2c_retriever.search(
        query_text=QUERY_TEXT
    )
    for item in result.items or []:
        print(item.content)
    print("\nCYPHER:\n")
    print(result.metadata['cypher'])