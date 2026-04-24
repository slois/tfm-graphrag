# Inspired from:
#  - https://medium.com/neo4j/hybrid-retrieval-for-graphrag-applications-using-the-neo4j-genai-python-package-fddfafe06ff3
#  - https://medium.com/neo4j/introducing-toolsretriever-in-the-neo4j-graphrag-python-package-04d0c3773f62

import logging

from neo4j_graphrag.generation import RagTemplate, GraphRAG
from neo4j_graphrag.retrievers import ToolsRetriever

from data.prompts import TOOLS_RETRIEVER_SYSTEM_INSTRUCTIONS, RAG_TEMPLATE
from src.core.tools.gene import got
from src.data_models.entity_recognition import QueryExtraction
from src.embedders import embedder
from src.graph.neo4j_client import driver, index_map
from src.llms import llm, ner_llm
from src.retrievers.entity_linker_retriever import EntityLinkingRetriever
from src.tools import disease_context_tool, gene_similarity_tool, disease_similarity_tool, disease_vector_context_tool, \
    one_hop_tool, multihop_tool, factual_tool

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Initializing GraphRAG pipeline")

    QUERY_TEXT = """
    autosomal dominant malformative disorder, is characterized by hypothalamic hamartoma, pituitary dysfunction, bifid epiglottis, polydactyly, and, more rarely, renal abnormalities and genitourinary malformations.
    """

    QUERY_TEXT = """Which are key phenotypes observed in Pallister-Hall syndrome patients? Could you retrieve phenotypes of 10 animal models of this disease"""

    QUERY_TEXT="""
    Based on the following Case Report, prioritize the most likely causal gene from this list of detected VUS: ASIC1, SHANK3, and SYNGAP1.

    Case Report: 6-year-old female, moderate intellectual disability, language delay, autistic behaviors, absence seizures, truncal hypotonia, and marked hypoalgesia (insensitivity to pain). Neuroimaging shows corpus callosum hypoplasia.
    """

    QUERY_TEXT="""
    Patient Description:
A 14-month-old male infant presents with refractory infantile spasms and profound global developmental delay. The patient achieved head control at 5 months but has since regressed, currently showing severe axial hypotonia and lack of social engagement.

Clinical Findings:

    Seizures: Daily tonic-clonic seizures that are resistant to first-line anticonvulsants (valproate and levetiracetam).

    Neurodevelopment: Moderate to severe intellectual disability (predicted), absent speech, and stereotypical hand movements.

    Laboratory/Metabolic: Plasma amino acid analysis reveals hyperlysinemia (elevated lysine levels) and increased pipecolic acid in cerebrospinal fluid (CSF).

    Imaging: MRI shows delayed myelination and slight cerebellar atrophy.

Genomic Findings (VUS detected):

    ALDH7A1 (HGNC:408)

    SCN1A (HGNC:10585)

    KCNQ2 (HGNC:6296)
    """

    QUERY_TEXT = """
    Patient: 7-year-old male with global developmental delay and intellectual disability.

    Phenotypes observed:
    - Moderate intellectual disability
    - Speech delay (single words only, no phrases)
    - Motor delay (walked at 28 months)
    - Mild microcephaly
    - Broad and angulated thumbs
    - Clinodactyly of the 5th finger
    - Arched eyebrows
    - Long eyelashes
    - Bulbous nose tip
    - Long philtrum
    - Wide mouth with thick lips
    - Large low-set ears
    - Axial hypotonia
    - History of febrile seizures
    - Stereotyped behaviors
    - Reduced social engagement

    Genomic findings (VUS detected by NGS panel):
    - CREBBP
    - KAT6A
    - ANKRD11

    Based on the clinical features and genomic findings, prioritize the most likely 
    causal gene and provide the differential diagnosis with supporting evidence 
    from the knowledge graph.
    """

    QUERY_TEXT = """
    A 7‐month‐old female infant was referred to genetics clinic for an evaluation of microcephaly, failure to thrive (FTT), and dysmorphic features. The patient was born at 38 weeks gestation to a 21‐year‐old mother with no history of prior pregnancy who had a history of nausea and preeclampsia throughout the pregnancy. She was delivered via cesarean section with Apgar scores of 8 and 9 after 1 and 5 min respectively. Birthweight (BW) was 2.24 kg, birth length was 47 cm. The patient was admitted to the Neonatal Intensive Care Unit for 1 week due to hypothermia, feeding issues, and jaundice which resolved without phototherapy. The patient received feeds via a nasogastric tube for 1 week after birth, then was discharged home, and followed by her pediatrician.
    On evaluation, the patient's weight was 5.89 kg (1st %), length was 62 cm (<1st %), and occipitofrontal head circumference (OFC) was 40.5 cm (2.8th %). The patient had microcephaly with bitemporal narrowing of the forehead, hirsutism, arched thick eyebrows, synophrys, bilateral epicanthal folds, long curly eyelashes, and mild ptosis. Her nose appeared short and upturned, with a flat nasal bridge. She also had a small oral cavity, high‐arched palate, and a small chin with mild retrognathia. Her limb examination showed proximally placed thumbs, bilateral fifth finger clinodactyly, small 4th and 5th metacarpals, and mild 2nd and 3rd toes syndactyly.
    Her neurological examination showed low generalized muscle bulk and hypotonia. There was no evidence of tremors or abnormal movements, and deep tendon reflexes were within normal limits. Developmentally, she sat independently at 7 months.
    On follow‐up examination at the age of 14 months, she was noted to have improved oral intake after feeding therapy. Her weight increased to 8.2 kg (10%), length measured 74 cm (15%), but OFC remained relatively small at 43 cm (5%). A developmental assessment carried out at that age showed she was advanced in her fine motor skills at 21 months of age, but gross motor skills were delayed at 11 months of age, and expressive language was at 12 months of age. She was able to pull herself up to stand and walked with support while leaning on the furniture. She began to walk independently by age 15 months.
    Because the patient was not babbling, she was receiving speech therapy through early intervention. Echocardiogram identified a trivial patent foramen oval, with a mild atrial left to right shunt. Renal ultrasound was normal. 
    What are the most probable disease and gene?
    """


    QUERY_TEXT="""
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

    QUERY_TEXT = """
    Which genes participate in pathways linked to diseases presenting lack of external genitalia ?
    """
    QUERY_TEXT = """
    Which phenotypes are associated with genes affected by the variant CLINVAR:254496?
    """

    QUERY_TEXT = """
    Which diseases are related to pathways in which the gene HGNC:4189 participates?
    """

    QUERY_TEXT = """
    Which phenotypes are associated with diseases caused by the gene HGNC:4019?
    """

    QUERY_TEXT = """
    Which pathways does the gene HGNC:4014 participate in?
    """

    QUERY_TEXT = """
    Which phenotypes are associated with the gene HGNC:4092?
    """

    QUERY_TEXT = """
    Which diseases are associated with the gene HGNC:4175?
    """

    QUERY_TEXT = """
    Which disease has 'peripheral neurofibromatosis' as synonym?
    """

    QUERY_TEXT = """
    Case report
    A pediatric patient presented with moderate intellectual disability, global developmental delay, and microcephaly. 
    The neonatal history was notable for a characteristic high-pitched, cat-like cry. Physical examination revealed 
    facial dysmorphism including hypertelorism and micrognathia.
    
    Could you assist me to diagnose this patient? I have a pathogenic mutation in PLXNA3 and I would like to explore:
     (A) the relationship of PLXNA3 gene and Cri-du-chat syndrome and,
     (B) similar phenotypes between Cri-du-chat and PLXNA3
    """

    QUERY_TEXT = "Which genes participate in biological process 'Reactome:R-HSA-445095' and are associated with diseases that present phenotype HP:0001328?"

    entity_linker = EntityLinkingRetriever(
        driver=driver, embedder=embedder, llm=ner_llm, entities_model=QueryExtraction, index_map=index_map
    )
    linked = entity_linker.get_search_results(query_text=QUERY_TEXT)

    ENRICHED_QUERY_TEXT = entity_linker.build_enriched_query(QUERY_TEXT, linked)

    tools_retriever = ToolsRetriever(
        driver=driver,
        llm=llm,
        tools=[
            factual_tool,
            one_hop_tool,
            multihop_tool,
            #disease_vector_context_tool,
            #gene_similarity_tool,
            #disease_similarity_tool,
            #disease_context_tool,
            #got
        ],
        system_instruction=TOOLS_RETRIEVER_SYSTEM_INSTRUCTIONS
    )

    # GraphRAG
    rag_template = RagTemplate(
        RAG_TEMPLATE,
        expected_inputs=["query_text", "context"]
    )

    graph_rag = GraphRAG(
        retriever=tools_retriever,
        llm=llm,
        prompt_template=rag_template
    )

    # Perform a search
    res = graph_rag.search(
        query_text=ENRICHED_QUERY_TEXT,
        return_context=True,
        response_fallback="I can not answer this question because I have no relevant context.",
        retriever_config={'top_k': 5, 'filters': None}
    )

    print(f"User: {ENRICHED_QUERY_TEXT}")
    print(f"Answer: {res.answer}")


