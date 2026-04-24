from src.graph.neo4j_client import driver

import logging
import os
import re
from typing import Any

from neo4j_graphrag.retrievers.base import Retriever
from neo4j_graphrag.types import RawSearchResult

from pydantic import BaseModel, Field
from typing import List


class PhenotypeExtraction(BaseModel):
    hpo_ids: List[str] = Field(default_factory=list,
                               description="Explicit HPO identifiers (HP:xxxxxxx) or (MP:xxxxxxx)")
    limit: int = Field(default=10, description="Number of results to return"),


class ParametricCypherRetriever(Retriever):
    """
    Retriever with fixed Cypher query that extracts parameters from the user query
    """

    CYPHER = None

    def __init__(self, driver):
        super().__init__(driver, os.getenv("NEO4J_DATABASE"))

    def _extract_params(self, query_text: str) -> dict:
        """
        Extracts parameters from the user query
        :param query_text:
        :return:
        """
        params = {"hpo_ids": [], "limit": 10}

        # Regular expression identification
        hpo_pattern = re.findall("[HM]P:[0-9]{7}", query_text)
        params["hpo_ids"] = hpo_pattern if hpo_pattern else []

        return params

    def get_search_results(self, query_text: str, **kwargs: Any) -> RawSearchResult:
        params = self._extract_params(query_text)
        logging.debug(f"params: {params}")

        if len(params["hpo_ids"]) == 0:
            return RawSearchResult(records=[], metadata={"params": params})

        with self.driver.session() as session:
            result = session.run(self.CYPHER, **params)
            records = list(result)

        return RawSearchResult(records=records, metadata={"params": params})

    def _fetch_records(self, query_text: str, **kwargs):
        return self.get_search_results(query_text, **kwargs)


class GeneParametricCypherRetriever(ParametricCypherRetriever):
    CYPHER = """
    // 1. Perfil del paciente
    WITH $hpo_ids AS hpo_set

    // 2. Por cada término del paciente, buscamos el mejor match en cada enfermedad
    UNWIND hpo_set AS p_id
    MATCH (p_paciente:`biolink:PhenotypicFeature` {id: p_id, namespace: 'HP'})

    MATCH (d:`biolink:Gene`)-[:`biolink:has_phenotype`]->(p_obj:`biolink:PhenotypicFeature` {namespace: 'HP'})

    // 3. Encontramos el ancestro común más informativo (MICA) entre el síntoma del paciente y el de la enfermedad
    MATCH (p_paciente)-[:`biolink:subclass_of`*0..]->(mica),
          (p_obj)-[:`biolink:subclass_of`*0..]->(mica)
    WHERE mica.IC_gene > 1.0

    // 4. Nos quedamos con el IC del MICA más alto para ese par
    WITH d, p_id, max(mica.IC_gene) AS max_ic_for_term 

    // 5. Promediamos los mejores ICs encontrados para todos los términos del paciente
    RETURN d.id AS gene_id, d.symbol AS gene_symbol, d.full_name AS gene_name, sum(max_ic_for_term) AS resnik_score
    ORDER BY resnik_score DESC

    LIMIT $limit
    """


class DiseaseParametricCypherRetriever(ParametricCypherRetriever):
    CYPHER = """
     // 1. Perfil del paciente
     WITH $hpo_ids AS hpo_set

     // 2. Por cada término del paciente, buscamos el mejor match en cada enfermedad
     UNWIND hpo_set AS p_id
     MATCH (p_paciente:`biolink:PhenotypicFeature` {id: p_id, namespace: 'HP'})

     MATCH (d:`biolink:Disease`)-[:`biolink:has_phenotype`]->(p_obj:`biolink:PhenotypicFeature` {namespace: 'HP'})

     // 3. Encontramos el ancestro común más informativo (MICA) entre el síntoma del paciente y el de la enfermedad
     MATCH (p_paciente)-[:`biolink:subclass_of`*0..]->(mica),
           (p_obj)-[:`biolink:subclass_of`*0..]->(mica)
     WHERE mica.IC_disease > 1.0

     // 4. Nos quedamos con el IC del MICA más alto para ese par
     WITH d, p_id, max(mica.IC_disease) AS max_ic_for_term 

     // 5. Promediamos los mejores ICs encontrados para todos los términos del paciente
     RETURN d.id AS disease_id, d.name AS disease_name, d.description AS disease_description, sum(max_ic_for_term) AS resnik_score
     ORDER BY resnik_score DESC

     LIMIT $limit
     """

rank_disease_retriever = DiseaseParametricCypherRetriever(driver=driver)
rank_gene_retriever = GeneParametricCypherRetriever(driver=driver)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")

    query_text = """
    Rank according on patient phenotypes: "HP:0001034", "HP:0100006", "HP:0001000", "HP:0000768", "HP:0000525", "HP:0009121", "HP:0032263", "HP:0001627"
    """
    res = rank_disease_retriever.search(query_text=query_text)
    for item in res.items:
        print(item)

    query_text = """
    Rank according on patient phenotypes: "HP:0001034", "HP:0100006", "HP:0001000", "HP:0000768", "HP:0000525", "HP:0009121", "HP:0032263", "HP:0001627"
    """
    res = rank_gene_retriever.search(query_text=query_text)
    for item in res.items:
        print(item)