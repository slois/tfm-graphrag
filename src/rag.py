import logging

from langchain_community.callbacks import get_openai_callback
from neo4j_graphrag.generation import RagTemplate, GraphRAG
from neo4j_graphrag.retrievers import ToolsRetriever

from data.prompts import TOOLS_RETRIEVER_SYSTEM_INSTRUCTIONS, RAG_TEMPLATE
from src.core.ner import NamedEntityRecognition
from src.data_models.entity_recognition import QueryExtraction
from src.embedders import embedder
from src.graph.neo4j_client import driver
from src.llms import ner_llm, llm
from src.tools import factual_tool, one_hop_tool, multihop_tool

# Inspired from:
#  - https://medium.com/neo4j/hybrid-retrieval-for-graphrag-applications-using-the-neo4j-genai-python-package-fddfafe06ff3
#  - https://medium.com/neo4j/introducing-toolsretriever-in-the-neo4j-graphrag-python-package-04d0c3773f62

class DiMonarchAnswer(object):
    def __init__(self, response, linked, query):
        self.response = response
        self.linked = linked
        self.query = query


class DiMonarchKG(object):
    def __init__(self):
        self.ner = NamedEntityRecognition(driver=driver, embedder=embedder, llm=ner_llm, model=QueryExtraction) #ner_llm

        tools_retriever = ToolsRetriever(
            driver=driver,
            llm=llm,
            tools=[factual_tool, one_hop_tool, multihop_tool],
            system_instruction=TOOLS_RETRIEVER_SYSTEM_INSTRUCTIONS
        )

        rag_template = RagTemplate(RAG_TEMPLATE, expected_inputs=["query_text", "context"])

        self.graph_rag = GraphRAG(retriever=tools_retriever, llm=llm, prompt_template=rag_template)

    def search(self, query_text: str, enrich: bool = True, return_context: bool = False, **kwargs):

        if enrich:
            query_text, linked = self.ner.enrich_query(query_text)
        else:
            linked = None

        with get_openai_callback() as cb:
            res = self.graph_rag.search(
                query_text=query_text,
                return_context=return_context,
                response_fallback="I can not answer this question because I have no relevant context.",
                retriever_config=kwargs
            )
            logging.info(
                "Input [{input_tk} Tk] | Output [{output_tk} Tk]".format(input_tk=cb.prompt_tokens, output_tk=cb.completion_tokens))

        #res.metadata['enriched_query'] = query_text

        return DiMonarchAnswer(response=res, linked=linked, query=query_text)
