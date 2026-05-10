import json

import pandas as pd

if __name__ == "__main__":
    RESULTS_JSON = "/tmp/benchmark_results_20260424.json"
    with open(RESULTS_JSON, "r") as fh:
        dataset = json.load(fh)

    df = pd.DataFrame(dataset['items'])
    df.loc[:, ['id', 'question', 'category', 'ground_truth', 'elapsed_time', 'tools_selected']].to_csv("/home/slois/Descargas/evaluation.csv", header=True, index=False)
