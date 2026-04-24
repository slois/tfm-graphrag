from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from data.prompts import TEXT_TO_CYPHER_PROMPT
from data.schemas import EXTENDED_NEO4J_SCHEMA as schema
from src.graph.neo4j_client import driver
from src.llms import llm

def formatter(r):
    res = RetrieverResultItem(
        content=", ".join(f"{k}: {v}" for k, v in r.data().items()),
        metadata=None)
    return res

t2c_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,
    custom_prompt=TEXT_TO_CYPHER_PROMPT,
    neo4j_schema=schema#,
    #result_formatter=formatter
)

if __name__ == "__main__":
    res = t2c_retriever.search(query_text="""
    Patient Description:
    A 4-day-old neonate presents with multiple daily episodes of focal seizures [HP:0007359, biolink:PhenotypicFeature] that quickly generalize. The pregnancy and delivery were unremarkable, but the onset of seizures within the first week of life has triggered an urgent evaluation.

    Clinical Findings:
    Seizure Type: Focal tonic seizures with cyanosis [HP:0000961, biolink:PhenotypicFeature].
    EEG: Shows a "burst-suppression" pattern, suggesting a severe early-onset encephalopathy.
    Development: Too early to assess, but the patient shows significant lethargy [UPHENO:7000238, biolink:PhenotypicFeature] between episodes.
    Response to Medication: The seizures show a paradoxical worsening when treated with Phenytoin (a sodium channel blocker).

    Genomic Findings (VUS detected):
    SCN1A [HGNC:10585, biolink:Gene] (HGNC:10585)
    SCN2A [HGNC:10588, biolink:Gene] (HGNC:10588)
    KCNQ2 [HGNC:6296, biolink:Gene] (HGNC:6296)
    """)
    print(res)