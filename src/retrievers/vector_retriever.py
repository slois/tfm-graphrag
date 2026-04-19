
from neo4j_graphrag.retrievers import HybridCypherRetriever, VectorCypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from src.embedders import embedder
from src.graph.neo4j_client import driver

query = """
MATCH (node)<-[r*1..2]-(neighbor)
UNWIND r as rel
RETURN node.id AS id, node.name AS name, node.description, collect(type(rel) + ' -> ' + neighbor.name + ' (' + neighbor.id +')') AS relationships
"""


def disease_context_formatter(record) -> RetrieverResultItem:
    data = record.data()

    disease_id   = data.get("id", "")
    disease_name = data.get("name", "")
    description  = data.get("node.description", data.get("description", ""))
    relationships = data.get("relationships", [])

    causal_genes = set()
    subtypes = set()

    for rel in relationships:
        # Solo relaciones causales directas — excluir interacts_with
        if rel.startswith("biolink:causes ->"):
            gene = rel.split("->")[1].strip()
            # Filtrar solo genes humanos (HGNC)
            if "HGNC:" in gene:
                causal_genes.add(gene)
        elif rel.startswith("biolink:gene_associated_with_condition ->"):
            gene = rel.split("->")[1].strip()
            if "HGNC:" in gene:
                causal_genes.add(gene)
        elif rel.startswith("biolink:subclass_of ->") and "MONDO:" in rel:
            subtype = rel.split("->")[1].strip()
            subtypes.add(subtype)

    content_parts = [f"Disease: {disease_name} ({disease_id})"]

    if description:
        content_parts.append(
            f"Description: {description[:400]}..."
            if len(description) > 400
            else f"Description: {description}"
        )

    if causal_genes:
        content_parts.append(
            f"Causal genes: {', '.join(sorted(causal_genes))}"
        )

    if subtypes:
        content_parts.append(
            f"Subtypes: {', '.join(sorted(subtypes))}"
        )

    return RetrieverResultItem(
        content="\n".join(content_parts),
        metadata={"disease_id": disease_id, "disease_name": disease_name}
    )

phenotype_retriever = VectorCypherRetriever(
    driver=driver,
    index_name="phenotypic_feature_index",
    #fulltext_index_name="phenotypic_feature_fulltext_index",
    embedder=embedder,
    # Cypher to expand retrieved nodes into their graph neighborhood
    retrieval_query=query,
    result_formatter=disease_context_formatter
)

disease_retriever = VectorCypherRetriever(
    driver=driver,
    index_name="disease_index",
    #fulltext_index_name="disease_fulltext_index",
    embedder=embedder,
    # Cypher to expand retrieved nodes into their graph neighborhood
    retrieval_query=query,
    result_formatter=disease_context_formatter
)

if __name__ == "__main__":
    enriched_query = """Which disease or genes are most likely to be associated with the observed phenotypes: An abnormal path of a coronary artery (HP:0011686, biolink:PhenotypicFeature), 
    Deviation from the norm of height (HP:0000002, biolink:PhenotypicFeature), 
    Abnormal functionality of the gastrointestinal tract (HP:0012719, biolink:PhenotypicFeature), 
    Displacement of the big toe (HP:0010051, biolink:PhenotypicFeature), 
    A broad range of compulsive behaviors are repeated (HP:0031432, biolink:PhenotypicFeature), 
    Abnormal position of urethral meatus on the ventral penile shaft (HP:0032076, biolink:PhenotypicFeature), 
    Obstruction of the flow of urine through the ureter (HP:0006000, biolink:PhenotypicFeature), 
    structural abnormality of a cardiac atrium (HP:0005120, biolink:PhenotypicFeature).

    PHENOTYPES=HP:0011686; HP:0000002; HP:0012719; HP:0010051; HP:0031432; HP:0032076; HP:0006000; HP:0005120"""

    result = disease_retriever.search(
        query_text=enriched_query,
        top_k=10
    )
    print("Retriever items:")
    for item in result.items:
        print(item)
    print("Retriever metadata:", result.metadata)