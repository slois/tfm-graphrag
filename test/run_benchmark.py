import logging
import time
import pandas as pd

from bin.main import DiMonarchKG
from test.build_benchmark import BenchmarkDataset, BenchmarkResult, BenchmarkResultItem

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
    logger = logging.getLogger(__name__)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)


    dataset = BenchmarkDataset.load_from_json("/home/slois/repos/tfm-graphrag/data/graphrag_evaluation_dataset_2.json")
    model = DiMonarchKG()


    br = BenchmarkResult()
    for item in dataset.items:
        logger.info(f"Q{item.id}: {item.question_instantiated}")
        start = time.time()
        answer = model.search(query_text=item.question_instantiated, return_context=True)
        end = time.time()
        logger.info(f"Answer: {answer.answer}")
        logger.info(f"Elapsed time: {end - start} seconds")
        logger.info(f"Expected answer: {item.ground_truth}")
        br.items.append(BenchmarkResultItem(
            id=item.id,
            question=item.question_instantiated,
            category=item.category,
            difficulty=item.difficulty,
            expected_answer_type=item.expected_answer_type,
            ground_truth=item.ground_truth,
            model_answer=answer.answer,
            elapsed_time=end - start,
            tools_selected=answer.retriever_result.metadata.get('tools_selected', [])
        ))
    br.save(output="/tmp/benchmark_results_20260424.json")
