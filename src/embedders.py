import os
import dotenv

from neo4j_graphrag.embeddings.sentence_transformers import SentenceTransformerEmbeddings


dotenv.load_dotenv()
embedder = SentenceTransformerEmbeddings(model=os.environ["EMBEDDING_MODEL_NAME"])