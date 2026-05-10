from typing import Dict, Tuple

from src.data_models.entity_linking import LinkedEntity, LinkStrategy


class EntityLinker(object):
    def __init__(self, driver, embedder, index_map: Dict[str, Tuple[str, str, str]]):
        self._driver = driver
        self._embedder = embedder
        self.index_map = index_map

    def link(self, mentions, threshold: float = 0.8):
        results = {k: [] for k in self.index_map.keys()}
        with self._driver.session() as session:
            for entity_type in self.index_map.keys():
                entities = getattr(mentions, entity_type)
                for mention in entities:
                    entity = self._link_single(session, mention.mention, entity_type, threshold)
                    results[entity_type].append(entity)
        return results

    def vector_search(self, session, mention: str, v_index: str, namespace: str, threshold: float, top_k: int):
        embedding = self._embedder.embed_query(mention)
        result = session.run(f"""
        CALL db.index.vector.queryNodes($index, $top_k, $emb)
        YIELD node, score
        WHERE score > $threshold AND node.namespace = $namespace
        RETURN node.id AS id, node.name AS name, node.namespace as namespace, score
        ORDER BY score DESC
        """, index=v_index, emb=embedding, threshold=threshold, top_k=top_k, namespace=namespace)
        return result.data()

    @staticmethod
    def fulltext_search(session, mention: str, ft_index: str, threshold: float = 1.0):
        result = session.run(f"""
                        CALL db.index.fulltext.queryNodes($index, $mention)
                        YIELD node, score
                        WHERE score > $threshold
                        RETURN node.id AS id, node.name AS name, score
                        ORDER BY score DESC
                    """, index=ft_index, mention=mention, threshold=threshold)
        return result.data()

    def _link_single(self, session, mention: str, entity_type: str, threshold: float):
        v_index, ft_index, label = self.index_map[entity_type]

        # Scenario 1: exact match using entity id
        result = session.run(f"""
            MATCH (n:`{label}`)
            WHERE toLower(n.name) = toLower($mention)
            RETURN n.id AS id, n.name AS name, 1.0 AS score
            LIMIT 1           
        """, mention=mention).single()

        if result:
            return LinkedEntity(mention=mention, node_id=result["id"], name=result["name"], label=label, score=1.0,
                                strategy=LinkStrategy.EXACT)

        # Scenario 2: fulltext
        if ft_index is not None:
            result = session.run(f"""
                            CALL db.index.fulltext.queryNodes($index, $mention)
                            YIELD node, score
                            WHERE score > 1.0
                            RETURN node.id AS id, node.name AS name, score
                            ORDER BY score DESC LIMIT 1
                        """, index=ft_index, mention=mention).single()

            if result:
                return LinkedEntity(
                    mention=mention, node_id=result["id"],
                    name=result["name"], label=label,
                    score=float(result["score"]), strategy=LinkStrategy.FULLTEXT
                )

        # Scenario 3: Vector search
        embedding = self._embedder.embed_query(mention)
        result = session.run(f"""
                    CALL db.index.vector.queryNodes($index, 3, $emb)
                    YIELD node, score
                    WHERE score > $threshold AND (node.namespace IS NULL OR node.namespace = 'HP') AND (node.in_taxon IS NULL OR node.in_taxon = 'NCBITaxon:9606')
                    RETURN node.id AS id, node.name AS name, score
                    ORDER BY score DESC LIMIT 1
                """, index=v_index, emb=embedding, threshold=threshold).single()

        if result:
            return LinkedEntity(
                mention=mention, node_id=result["id"],
                name=result["name"], label=label,
                score=float(result["score"]), strategy=LinkStrategy.VECTOR
            )

        return LinkedEntity(mention=mention, node_id=None, name=mention, label=label, score=0.0,
                            strategy=LinkStrategy.NONE)


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
    - diseases: named syndromes or disorders
    - gene: gene symbols or names

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