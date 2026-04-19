import os
import dotenv

from langchain_openai import ChatOpenAI
from neo4j_graphrag.llm.openai_llm import OpenAILLM

dotenv.load_dotenv(override=True)

llm = OpenAILLM(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name=os.environ.get("OPENAI_MODEL_NAME"),
    model_params={'temperature': 0.0}
)

ner_llm = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model=os.environ.get("OPENAI_MODEL_NAME"),
    temperature=0.0
)