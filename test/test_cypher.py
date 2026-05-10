import json

import pandas as pd
from neo4j_graphrag.exceptions import Text2CypherRetrievalError
from neo4j_graphrag.retrievers import Text2CypherRetriever

from src.retrievers.context_retriever import t2c_context_retriever
from src.retrievers.factual_retriever import factual_retriever
from src.retrievers.multihop_retriever import multihop_t2c_retriever
from test.build_benchmark import BenchmarkDataset, QuestionCategory

if __name__ == '__main__':

    dataset = BenchmarkDataset.load_from_json("/home/slois/repos/tfm-graphrag/data/graphrag_evaluation_dataset_2.json")

    data = list()
    for item in dataset.items:
        result = None
        if item.category in [QuestionCategory.MULTI_HOP, QuestionCategory.MULTI_ENTITY]:
            ret = multihop_t2c_retriever
        elif item.category == QuestionCategory.ONE_HOP:
            ret = t2c_context_retriever
        elif item.category == QuestionCategory.FACTUAL:
            ret = factual_retriever
        else:
            ret = None

        if ret is not None:
            try:
                result = ret.search(query_text=item.question_instantiated)
                if result is not None:
                    data.append(
                        dict(id=item.id, question=item.question_instantiated, expected_cypher=item.subgraph_cypher,
                             cypher=result.metadata['cypher']))
            except Text2CypherRetrievalError:
                data.append(dict(id=item.id, question=item.question_instantiated, expected_cypher=item.subgraph_cypher,
                                 cypher='TEXT2CYPHER_ERROR'))
        else:
            data.append(dict(id=item.id, question=item.question_instantiated, expected_cypher=item.subgraph_cypher, cypher='RETRIEVER_ERROR'))

    with open("/home/slois/repos/tfm-graphrag/data/cypher_structural_correctness.json", "w") as j:
        json.dump(data, j, indent=4)