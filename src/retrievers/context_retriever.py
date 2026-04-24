from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.types import RetrieverResultItem

from data.fewshots import NEIGHBORHOOD_EXAMPLES
from data.prompts import TEXT_TO_CYPHER_PROMPT
from data.schemas import NEIGHBORHOOD_SCHEMA
from src.graph.neo4j_client import driver
from src.llms import llm, t2c_llm


def neighborhood_formatter(record) -> RetrieverResultItem:
    data = record.data()

    entity_id   = data.get("entity_id", "")
    entity_name = data.get("entity_name", "")
    entity_type = data.get("entity_type", "")

    parts = [f"## {entity_type}: {entity_name} ({entity_id})"]

    # Campos opcionales según tipo de entidad
    field_labels = {
        "full_name":              "Full name",
        "description":            "Description",
        "symbol":                 "Symbol",
        "ic":                     "Information Content",
        "phenotypes":             "Phenotypes",
        "gene_phenotypes":        "Gene phenotypes",
        "disease_phenotypes":     "Disease phenotypes",
        "diseases":               "Associated diseases",
        "causal_genes":           "Causal genes",
        "inheritance":            "Inheritance",
        "variants":               "Variants",
        "ancestors":              "HPO ancestors",
        "children":               "HPO children",
        "diseases_with_phenotype":"Diseases with this phenotype",
    }

    for field, label in field_labels.items():
        value = data.get(field)
        if not value:
            continue
        if isinstance(value, list):
            clean = [v for v in value if v]
            if clean:
                # Truncar descripción
                if field == "description" and len(str(clean[0])) > 300:
                    parts.append(f"{label}: {str(clean[0])[:300]}...")
                else:
                    parts.append(f"{label}: {', '.join(str(v) for v in clean)}")
        elif value:
            text = str(value)
            if field == "description" and len(text) > 300:
                text = text[:300] + "..."
            parts.append(f"{label}: {text}")

    return RetrieverResultItem(
        content="\n".join(parts),
        metadata={"entity_id": entity_id, "entity_type": entity_type}
    )

t2c_context_retriever = Text2CypherRetriever(
    driver=driver,
    llm=t2c_llm,
    custom_prompt=TEXT_TO_CYPHER_PROMPT,
    neo4j_schema=NEIGHBORHOOD_SCHEMA,
    examples=NEIGHBORHOOD_EXAMPLES,
    #result_formatter=neighborhood_formatter
)

if __name__ == '__main__':
    res = t2c_context_retriever.search(query_text="""
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
    """)

    for item in res.items:
        print(item)