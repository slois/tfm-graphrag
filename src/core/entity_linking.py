import json
import re
from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel

from src.data_models.entity_recognition import QueryExtraction
from src.embedders import embedder
from src.graph.neo4j_client import driver, index_map
from src.llms import ner_llm
from src.retrievers.phenotypic_similarity_retriever import PhenotypeExtraction


class Source(str, Enum):
    REGEX = "regex"
    EXACT = "exact"
    VECTOR = "vector"
    HYBRID = "hybrid"

class Entity(BaseModel):
    id: str
    name: str
    label: str
    score: float
    source: Source

class LinkedEntity(BaseModel):
    mention: str
    candidates: List[Entity]
    selected: Optional[Entity]

class ELResults(BaseModel):
    entities: List[LinkedEntity]

ID_PATTERNS = {
    "biolink:Disease": r"(MONDO:[0-9]{7})",
    "biolink:PhenotypicFeature": r"(HP:[0-9]{7})",
    "biolink:Gene": r"(HGNC:\d+)"
}

class MentionExtractor(object):
    PROMPT = """Extract biomedical entity mentions from the user query.
    Return ONLY valid JSON, no explanation:
    {{
        "biolink:PhenotypicFeature": ["mention1", "mention2"],
        "biolink:Disease": ["mention1"],
        "biolink:Gene": ["mention1", "mention2"]
    }}
    Rules:
    - phenotypes: clinical signs, symptoms, HPO terms
    - diseases: named syndromes or disorders, MONDO terms
    - gene: gene symbols or names, HGNC ids

    Query: {query_text}
    """

    def __init__(self, llm, entities_model):
        self._llm = llm
        self._entities_model = entities_model
        self._extractor = self._llm.with_structured_output(self._entities_model)

    def extract_entities(self, query_text: str):
        prompt = self.PROMPT.format(query_text=query_text)
        response = self._extractor.invoke(prompt)
        return response



class EntityLinking(object):
    def __init__(self, driver, embedder):
        self.driver = driver
        self.embedder = embedder
        self.index_map = {
            'biolink:PhenotypicFeature': 'phenotypic_feature_index',
            'biolink:Disease': 'disease_index',
            'biolink:Gene': 'gene_index'
        }

    def validate_id(self, entity_id: str):
        query = "MATCH (n {id: $id}) RETURN n.id as id, n.name as name"
        with self.driver.session() as session:
            res = session.run(query, id=entity_id).single()
            return res

    def regexp_link(self, query: str):
        matches = []
        for label, pattern in ID_PATTERNS.items():
            for m in re.findall(pattern, query):
                node = self.validate_id(m)
                if node is not None:
                    matches.append(Entity(id=m, name=node['name'], label=label, score=1.0, source=Source.REGEX))
        return matches

    def exact_match_link(self, query: str, label: str, namespace: str):
        cypher = f"""
        MATCH (n:`{label}`)
        WHERE n.namespace = $namespace AND (toLower(n.name) = toLower($q) OR any(s IN n.exact_synonym WHERE toLower(s) = toLower($q)))
        RETURN n.id as id, n.name as name
        LIMIT 5
        """

        with self.driver.session() as session:
            results = session.run(cypher, q=query, namespace=namespace)
            return [Entity(id=r["id"], name=r["name"], label=label, score=0.95, source=Source.EXACT) for r in results]

    def vector_search_link(self, query: str, label: str, index: str, namespace: str, k: int = 5):
        cypher = f"""
        CALL db.index.vector.queryNodes('{index}', $k, $embedding)
        YIELD node, score
        WHERE node.namespace = $namespace
        RETURN node.id as id, node.name as name, score
        """

        embedding = self.embedder.embed_query(query)  # tu modelo

        with driver.session() as session:
            results = session.run(cypher, k=k, embedding=embedding, namespace=namespace)
            return [Entity(id=r["id"], name=r["name"], label=label, score=r["score"], source=Source.VECTOR) for r in results]

    def link_mention(self, mention, namespace):
        candidates = self.regexp_link(mention.mention)
        if not candidates:
            candidates += self.exact_match_link(mention.mention, label=mention.type, namespace=namespace)
        if not candidates:
            candidates += self.vector_search_link(mention.mention, label=mention.type, namespace=namespace,
                                                  index=self.index_map[mention.type], k=3)

        return LinkedEntity(mention=mention.mention, candidates=candidates, selected=candidates[0] if len(candidates) > 0 else None)

    def linking(self, mentions: List) -> ELResults:
        entities: List[LinkedEntity] = []
        for mention in mentions:
            if mention.type == 'biolink:PhenotypicFeature':
                ns = 'HP'
            elif mention.type == 'biolink:Disease':
                ns = 'MONDO'
            else:
                ns = 'HGNC'
            entities.append(self.link_mention(mention, namespace=ns))
        return ELResults(entities=entities)

class EnrichText(object):

    @staticmethod
    def insert_substring(source, insert, position):
        return source[:position] + " " + insert + source[position:]

    @staticmethod
    def replace_substrings(text, replacements, insert_formatter):
        for rep in replacements:
            pattern = rf"\b{rep['mention']}\b(?![^\[]*\])"
            matches = re.finditer(pattern, text)

            for m in matches:
                pos = m.span()[1]
                text = EnrichText.insert_substring(text, insert_formatter(rep), pos)
        return text

    @staticmethod
    def build_enriched_query(text: str, linked: ELResults, labels: Dict[str, str]):
        info = {l: [] for l in labels.keys()}
        info['replacements'] = []

        for label in labels:
            entities = list(map(lambda item: dict(
                mention=item.mention, label=item.selected.label, type=item.selected.source,
                id=item.selected.id, name=item.selected.name,
                score=item.selected.score),
                     filter(lambda item: item.selected and item.selected.label == label, linked.entities)))
            info['replacements'] += entities
            info[label] = list(map(lambda e: e['id'], entities))

        new_query = EnrichText.replace_substrings(
            text,
            replacements=info['replacements'],
            insert_formatter=lambda x: f"[{x['id']}, {x['label']}]"
        )

        new_query = f"{new_query}\n\n--- Resolved entities"
        for l, k in labels.items():
            new_query = f"{new_query}\n{k}=[{', '.join(info[l])}]"

        return new_query


if __name__ == '__main__':
    query_text = """
    Patient Description:
    A 14-month-old male infant presents with refractory infantile spasms and profound global developmental delay. 
    The patient achieved head control at 5 months but has since regressed, currently showing severe axial hypotonia and 
    lack of social engagement.

    Clinical Findings:
    - Seizures: Daily tonic-clonic seizures that are resistant to first-line anticonvulsants 
      (valproate and levetiracetam).
    - Neurodevelopment: Moderate to severe intellectual disability (predicted), absent speech, and 
      stereotypical hand movements.
    - Laboratory/Metabolic: Plasma amino acid analysis reveals hyperlysinemia (elevated lysine levels) and 
      increased pipecolic acid in cerebrospinal fluid (CSF).
    - Imaging: MRI shows delayed myelination and slight cerebellar atrophy.

    Genomic Findings (VUS detected):
    - ALDH7A1
    - SCN1A
    - KCNQ2
    """

    extractor = MentionExtractor(llm=ner_llm, entities_model=QueryExtraction)
    mentions = extractor.extract_entities(query_text)

    # index_map = {
    #     'biolink:PhenotypicFeature': 'phenotypic_feature_index',
    #     'biolink:Disease': 'disease_index',
    #     'biolink:Gene': None
    # }

    linker = EntityLinking(driver=driver, embedder=embedder)
    linked = linker.linking(mentions=mentions)

    enriched_query = EnrichText.build_enriched_query(
        text=query_text,
        linked=linked,
        labels={
            'biolink:PhenotypicFeature': 'hpo_ids',
            'biolink:Disease': 'mondo_ids',
            'biolink:Gene': 'hgnc_ids'
        }
    )

    for entity in linked.entities:
        print(entity.mention)
        for c in entity.candidates:
            print(f" -->  {c.id} {c.name} {c.label} {c.score} {c.source}")

    print(enriched_query)
