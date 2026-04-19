# Inspired from:
#  - https://medium.com/neo4j/hybrid-retrieval-for-graphrag-applications-using-the-neo4j-genai-python-package-fddfafe06ff3
#  - https://medium.com/neo4j/introducing-toolsretriever-in-the-neo4j-graphrag-python-package-04d0c3773f62

import logging

from neo4j_graphrag.generation import RagTemplate, GraphRAG
from neo4j_graphrag.retrievers import ToolsRetriever

from data.prompts import TOOLS_RETRIEVER_SYSTEM_INSTRUCTIONS, RAG_TEMPLATE
from src.data_models.entity_recognition import QueryExtraction
from src.embedders import embedder
from src.graph.neo4j_client import driver, index_map
from src.llms import llm, ner_llm
from src.retrievers.entity_linker_retriever import EntityLinkingRetriever
from src.tools import disease_context_tool

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Initializing GraphRAG pipeline")

    QUERY_TEXT = """
    autosomal dominant malformative disorder, is characterized by hypothalamic hamartoma, pituitary dysfunction, bifid epiglottis, polydactyly, and, more rarely, renal abnormalities and genitourinary malformations.
    """
    entity_linker = EntityLinkingRetriever(
        driver=driver, embedder=embedder, llm=ner_llm, entities_model=QueryExtraction, index_map=index_map
    )
    linked = entity_linker.get_search_results(query_text=QUERY_TEXT)

    ENRICHED_QUERY_TEXT = entity_linker.build_enriched_query(QUERY_TEXT, linked)

    tools_retriever = ToolsRetriever(  # WithEntityLinker(
        driver=driver,
        llm=llm,
        tools=[
            #basic_retriever_tool,
            # disease_phenotype_tool,
            # gene_disease_tool,
            #rank_genes_tool,
            #rank_diseases_tool
            disease_context_tool
            # phenotype_context_tool
        ],
        system_instruction=TOOLS_RETRIEVER_SYSTEM_INSTRUCTIONS
    )

    # GraphRAG
    rag_template = RagTemplate(RAG_TEMPLATE, expected_inputs=["query_text", "context"])
    graph_rag = GraphRAG(retriever=tools_retriever, llm=llm, prompt_template=rag_template)

    # Perform a search
    res = graph_rag.search(
        query_text=ENRICHED_QUERY_TEXT,
        return_context=True,
        response_fallback="I can not answer this question because I have no relevant context.",
        retriever_config={'top_k': 5, 'filters': None}
    )

    print(f"User: {ENRICHED_QUERY_TEXT}")
    print(f"Answer: {res.answer}")


