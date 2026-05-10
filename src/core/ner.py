from src.core.entity_linking import MentionExtractor, EntityLinking, EnrichText
from src.graph.neo4j_client import index_map


class NamedEntityRecognition(object):
    def __init__(self, driver, embedder, llm, model):
        # New
        self.extractor = MentionExtractor(llm=llm, entities_model=model)
        self.linker = EntityLinking(driver=driver, embedder=embedder)


    def enrich_query(self, query_text: str):
        mentions = self.extractor.extract_entities(query_text)
        linked = self.linker.linking(mentions=mentions)
        enriched_query = EnrichText.build_enriched_query(text=query_text, linked=linked,
            labels={
                'biolink:PhenotypicFeature': 'hpo_ids',
                'biolink:Disease': 'mondo_ids',
                'biolink:Gene': 'hgnc_ids'
            }
        )
        return enriched_query