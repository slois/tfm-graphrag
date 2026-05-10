### These queries and its classification has been designed using GPT-5.3
# "All evaluation queries are guaranteed to correspond to valid subgraphs sampled from the underlying knowledge graph, eliminating template-induced sparsity bias."
import json
import random
from enum import Enum
from typing import Dict, List, Any, Optional

from neo4j.exceptions import CypherSyntaxError
from pydantic import BaseModel, Field
from tqdm import tqdm

from src.graph.neo4j_client import driver

class QuestionCategory(str, Enum):
    FACTUAL = "factual"
    ONE_HOP = "one_hop"
    MULTI_HOP = "multi_hop"
    MULTI_ENTITY = "multi_entity"

class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"

class AnswerType(str, Enum):
    STRING = "string"
    LIST = "list"

# class ReasoningPaths(BaseModel):
#     path: List[str]
#     relations: List[str]

class BenchmarkEntry(BaseModel):
    id: int
    question: str
    category: QuestionCategory
    difficulty: QuestionDifficulty
    params: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    query_params: Optional[Dict[str, str]] = Field(default_factory=dict)
    cypher_template: str
    expected_answer_type: AnswerType
    reasoning_paths: List[Dict[str, Any]]
    subgraph_cypher: str
    ground_truth: Optional[List[str]] = Field(default_factory=list)

    @property
    def question_instantiated(self) -> str:
        question = self.question
        for k, v in self.query_params.items():
            question = question.replace(f"{{{k}}}", v)
        return question


class BenchmarkDataset(BaseModel):
    items: List[BenchmarkEntry]

    @classmethod
    def load_from_json(cls, file: str) -> "BenchmarkDataset":
        with open(file, 'r') as j:
            entry_data = json.load(j)
            return BenchmarkDataset(items=entry_data)

class BenchmarkResultItem(BaseModel):
    id: int
    question: str
    category: QuestionCategory
    difficulty: QuestionDifficulty
    expected_answer_type: AnswerType
    ground_truth: List[str]
    model_answer: str
    elapsed_time: float
    tools_selected: List[str]

class BenchmarkResult(BaseModel):
    items: Optional[List[BenchmarkResultItem]] = Field(default_factory=list)

    def save(self, output: str):
        with open(output, 'w') as out:
            json.dump(self.model_dump(), out, indent=2)


def sample_nodes(session, label, n=50):
    if label == "biolink:Gene":
        query = f"""
        MATCH (n:`{label}`)
        WHERE n.id IS NOT NULL AND n.in_taxon='NCBITaxon:9606'
        RETURN n.id AS id
        LIMIT {n}
        """
    else:
        query = f"""
        MATCH (n:`{label}`)
        WHERE n.id IS NOT NULL
        RETURN n.id AS id
        LIMIT {n}
        """
    return [r["id"] for r in session.run(query)]


def get_entity_pools(driver, entity_map: Dict[str, str]):
    entity_pools: Dict[str, List[str]] = dict()
    with driver.session() as session:
        for entity, label in entity_map.items():
            entity_pools[entity] = session.execute_read(sample_nodes, label, 50)
    return entity_pools

def instantiate_params(template, pools):
    params = {}

    for entity, values in pools.items():
        key = f"{entity}_id"
        if f"${key}" in template and pools[entity]:
            params[key] = random.choice(values)

        if "$gene_id_1" in template and "$gene_id_2" in template:
            g1, g2 = random.sample(pools["gene"], 2)
            params["gene_id_1"] = g1
            params["gene_id_2"] = g2
    return params

def run_cypher(session, query, params):
    result = session.run(query, **params)
    return [record.data() for record in result]

def execute_query(driver, query, params):
    with driver.session() as session:
        return session.execute_read(run_cypher, query, params)

def extract_subgraph(tx, subgraph_query, params):
    result = tx.run(subgraph_query, **params)

    subgraphs = []

    for record in result:
        if "p" not in record:
            continue

        p = record["p"]

        edges_seen = set()
        edges = []

        for rel in p.relationships:
            edge_key = (
                rel.start_node.get("id"),
                rel.end_node.get("id"),
                rel.type
            )

            if edge_key not in edges_seen:
                edges_seen.add(edge_key)
                edges.append({
                    "type": rel.type,
                    "source": rel.start_node.get("id"),
                    "target": rel.end_node.get("id")
                })

        nodes = [
            {
                "id": node.get("id"),
                "label": node.labels.pop() if node.labels else None
            }
            for node in p.nodes
        ]

        subgraphs.append({
            "nodes": nodes,
            "edges": edges
        })

    return subgraphs


def get_subgraph(driver, query, params):
    with driver.session() as session:
        return session.execute_read(extract_subgraph, query, params)

def normalize_answer(records):
    if not records:
        return []

    # flatten values
    values = []
    for r in records:
        for v in r.values():
            if isinstance(v, list):
                values.extend(v)
            else:
                if v is not None and v not in values:
                    values.append(v)

    # limpiar None + duplicados
    return [v for v in values if v is not None]

def build_ground_truth(dataset: BenchmarkDataset, pools, max_tries: int =50):
    enriched = []
    skipped = []

    for item in tqdm(dataset.items):
        success = False

        for _ in range(max_tries):
            if item.params:
                params = random.choice(item.params)
            else:
                params = instantiate_params(item.cypher_template, pools)

            try:
                raw = execute_query(driver, item.cypher_template, params)
                answer = normalize_answer(raw)

                if not answer:
                    continue

                subgraph = get_subgraph(driver, item.subgraph_cypher, params)

                enriched.append({
                    **item.__dict__,
                    "query_params": params,
                    "ground_truth": answer,
                    "subgraph_ground_truth": subgraph
                })

                success = True
                break

            except Exception as err:
                continue

        if not success:
            skipped.append(item.id)

    return enriched, skipped



def merge_subgraphs(subgraphs):
    nodes = {}
    edges = set()

    for sg in subgraphs:
        for n in sg["nodes"]:
            nodes[n["id"]] = n

        for e in sg["edges"]:
            edges.add((e["source"], e["type"], e["target"]))

    return {
        "nodes": list(nodes.values()),
        "edges": [
            {"source": s, "type": t, "target": o}
            for (s, t, o) in edges
        ]
    }


def compute_coverage(enriched, total):
    return len(enriched) / total

def main():
    print("Loading dataset...")
    dataset = BenchmarkDataset.load_from_json("../data/benchmark.json")

    entities_label_map = {
        'gene': 'biolink:Gene',
        'disease': 'biolink:Disease',
        'phenotype': 'biolink:PhenotypicFeature',
        'variant': 'biolink:SequenceVariant',
        'anatomy': 'biolink:AnatomicalEntity',
        'process': 'biolink:BiologicalProcess',
        'pathway': 'biolink:Pathway'
    }

    print("Sampling entity pools...")
    pools = get_entity_pools(driver, entities_label_map)

    print("Building ground truth...")
    enriched, skipped = build_ground_truth(dataset, pools, max_tries=100)

    coverage = compute_coverage(enriched, len(dataset.items))

    print(f"\nTest coverage: {coverage*100:.2f} % | Skipped tests: {skipped}")

    print("Saving output...")
    with open("../data/graphrag_evaluation_dataset_2.json", "w") as f:
        json.dump(enriched, f, indent=2)

    print("Done.")


if __name__ == "__main__":
    main()
    # entities_label_map = {
    #     'gene': '`biolink:Gene`',
    #     'disease': '`biolink:Disease`',
    #     'phenotype': '`biolink:PhenotypicFeature`',
    #     'variant': '`biolink:SequenceVariant`',
    #     'anatomy': '`biolink:AnatomicalEntity`',
    #     'process': '`biolink:BiologicalProcess`',
    #     'pathway': '`biolink:Pathway`'
    # }
    #
    # pools = get_entity_pools(driver, entities_label_map)
    #
    # dataset = BenchmarkDataset.load_from_json("../data/benchmark.json")
    #
    # final_dataset = build_ground_truth(driver, dataset, pools, max_tries=50)
    #
    # with open("../data/graphrag_evaluation_dataset_1.json", "w") as f:
    #     json.dump(final_dataset, f, indent=2)


    # t = benchmark.items[0].cypher_template
    # params = (instantiate_question(t, pools))
    # res = run_cypher(driver.session(), t, params)
    # print(res)




