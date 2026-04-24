from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from data.fewshots import MULTIHOP_EXAMPLES
from data.schemas import MULTIHOP_SCHEMA
from src.graph.neo4j_client import driver
from src.llms import t2c_llm


def multihop_formatter(record) -> RetrieverResultItem:
    """
    Formatea resultados de queries multi-hop en texto estructurado.
    Maneja dinámicamente cualquier combinación de columnas.
    """
    data = record.data()

    # Construir texto limpio desde los campos disponibles
    parts = []
    for key, value in data.items():
        if value is None or value == [] or value == "":
            continue
        if isinstance(value, list):
            clean = [str(v) for v in value if v]
            if clean:
                parts.append(f"{key}: {', '.join(clean)}")
        else:
            parts.append(f"{key}: {value}")

    return RetrieverResultItem(
        content=" | ".join(parts),
        metadata={"raw": data}
    )


# ── Retriever ──────────────────────────────────────────────────────────────────

multihop_t2c_retriever = Text2CypherRetriever(
    driver=driver,
    llm=t2c_llm,
    neo4j_schema=MULTIHOP_SCHEMA,
    examples=MULTIHOP_EXAMPLES,
    neo4j_database="dimonarchkg",
    result_formatter=multihop_formatter
)

if __name__ == "__main__":
    QUERY_TEXT = """
    Patient Description:
    A 4-day-old neonate presents with multiple daily episodes of focal seizures [HP:0007359, biolink:PhenotypicFeature] that quickly generalize. The pregnancy and delivery were unremarkable, but the onset of seizures within the first week of life has triggered an urgent evaluation.

    Clinical Findings:
    Seizure Type: Focal tonic seizures with cyanosis [HP:0000961, biolink:PhenotypicFeature].
    EEG: Shows a "burst-suppression" pattern, suggesting a severe early-onset encephalopathy [HP:0007105, biolink:PhenotypicFeature].
    Development: Too early to assess, but the patient shows significant lethargy [HP:0001254, biolink:PhenotypicFeature] between episodes.
    Response to Medication: The seizures show a paradoxical worsening when treated with Phenytoin (a sodium channel blocker).

    Genomic Findings (VUS detected):
    SCN1A [HGNC:10585, biolink:Gene] (HGNC:10585)
    SCN2A [HGNC:10588, biolink:Gene] (HGNC:10588)
    KCNQ2 [HGNC:6296, biolink:Gene] (HGNC:6296)
    
    - Retrieve gene - disease - phenotype evidence
    - Extract cross-species evidence from mouse orthologs (if possible)
    - Cases in the graph with similar phenotype profile (if available)
    """

    result = multihop_t2c_retriever.search(
        query_text=QUERY_TEXT
    )
    for item in result.items or []:
        print(item.content)