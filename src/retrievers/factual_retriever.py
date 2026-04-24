from neo4j_graphrag.retrievers import Text2CypherRetriever

from data.fewshots import FACTUAL_EXAMPLES
from data.prompts import FACTUAL_PROMPT
from data.schemas import FACTUAL_SCHEMA
from src.graph.neo4j_client import driver
from src.llms import t2c_llm

factual_retriever = Text2CypherRetriever(
    driver=driver,
    llm=t2c_llm,
    #custom_prompt=FACTUAL_PROMPT,
    neo4j_schema=FACTUAL_SCHEMA,
    examples=FACTUAL_EXAMPLES,
)
