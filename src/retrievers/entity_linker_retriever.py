from typing import Any

from neo4j_graphrag.retrievers.base import Retriever
from neo4j_graphrag.types import RawSearchResult

from src.core.entity_recognition import MentionExtractor, EntityLinker
from src.helpers import replace_substrings


class EntityLinkingRetriever(Retriever):
    """
    A custom retriever that normalises entities in the user’s text and enriches the query with graph IDs.
    It is always executed as a preliminary step before ToolsRetriever.
    """

    def __init__(self, driver, embedder, llm, entities_model, index_map):
        super().__init__(driver=driver)
        self.extractor = MentionExtractor(llm=llm, entities_model=entities_model)
        self.linker = EntityLinker(driver=driver, embedder=embedder, index_map=index_map)

    @staticmethod
    def _build_enriched_query(query_text, linked):
        lines = [query_text, "\n[Resolved entities:"]
        for etype, entities in linked.items():
            for e in entities:
                lines.append(f"{etype}: '{e.mention}' → {e.node_id} ({e.name}) [{e.strategy}]")
        lines.append("]")
        return "\n".join(lines)

    @staticmethod
    def build_enriched_query(query_text, linked):

        phenotypes = list(map(lambda e: dict(mention=e.mention, node_id=e.node_id, label=e.label),
                              filter(lambda i: i.node_id is not None, linked.metadata['entities']['phenotype'])))
        phenotype_onto_terms = list(map(lambda e: e['node_id'], phenotypes))

        diseases = list(map(lambda e: dict(mention=e.mention, node_id=e.node_id, label=e.label),
                            filter(lambda i: i.node_id is not None, linked.metadata['entities']['disease'])))
        disease_onto_terms = list(map(lambda e: e['node_id'], diseases))

        genes = list(map(lambda e: dict(mention=e.mention, node_id=e.node_id, label=e.label),
                         filter(lambda i: i.node_id is not None, linked.metadata['entities']['gene'])))
        gene_ids = list(map(lambda e: e['node_id'], genes))

        enriched_query = replace_substrings(query_text, replacements=phenotypes + diseases + genes,
                                            insert_formatter=lambda x: f"[{x['node_id']}, {x['label']}]")

        if len(phenotype_onto_terms) > 0:
            enriched_query = f"{enriched_query}\nPHENOTYPES={'; '.join(phenotype_onto_terms)}\n"

        if len(disease_onto_terms) > 0:
            enriched_query = f"{enriched_query}\nDISEASES={'; '.join(disease_onto_terms)}"

        if len(gene_ids) > 0:
            enriched_query = f"{enriched_query}\nGENES={'; '.join(gene_ids)}"

        return enriched_query

    def get_search_results(self, query_text: str, **kwargs: Any) -> RawSearchResult:
        # Extract mentions to entities
        mentions = self.extractor.extract_entities(query_text=query_text)

        # Link mentions to graph entities
        linked = self.linker.link(mentions, threshold=0.8)

        # Context building
        lines = []
        for etype, entities in linked.items():
            for e in entities:
                lines.append(f"{etype}: '{e.mention}' -> {e.node_id} ({e.name}) [{e.strategy}]")

        content = ("Normalized entities:\n" + "\n".join(lines) if lines else "No entities resolved.")

        # Entities storage for downstream usage
        return RawSearchResult(
            records=[],
            metadata={
                "entities": linked,
                "enriched_query": self._build_enriched_query(query_text, linked),
                "entity_context": content
            }
        )