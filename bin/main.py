

import logging

import pandas as pd

from src.rag import DiMonarchKG

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    logger.info("Initializing GraphRAG pipeline")

    QUERY_TEXT = """
    Which genes participate in biological process Reactome:R-HSA-9656223 and are associated with diseases that present phenotype HP:0004493?
    """

    model = DiMonarchKG()
    print(f"--- USER ---\n"
          f"{QUERY_TEXT}")
    answer = model.search(query_text=QUERY_TEXT, return_context=True)


    if answer is not None:
        print(f"\n--- ANSWER ---\n"
              f"{answer.answer}\n")

        print(f"\n--- TOOLS RETRIEVER ---\n"
              f"{answer.retriever_result.metadata['tools_selected']}")

        print(f"\n--- CONTEXT ---\n")
        context_df = []
        for item in answer.retriever_result.items:
            context_df.append(item.metadata['raw'])
            #print(f"METADATA: {item.metadata}")
        print(pd.DataFrame(context_df))




