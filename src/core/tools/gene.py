from neo4j_graphrag.tool import Tool, ObjectParameter, StringParameter, ArrayParameter

from src.graph.neo4j_client import driver

def phenotype_orthologs(hgnc_ids: str):
    with driver.session() as session:
        res = session.run("""
        MATCH (g:`biolink:Gene`)-[r:`biolink:orthologous_to`]->(o:`biolink:Gene`) WHERE g.id IN $hgnc_ids
        OPTIONAL MATCH (o)-[rh:`biolink:has_phenotype`]->(mp:`biolink:PhenotypicFeature`)
        OPTIONAL MATCH (mp)-[:`biolink:homologous_to`|`biolink:same_as`]-(hp:`biolink:PhenotypicFeature` {namespace: 'HP'})
        RETURN DISTINCT g.id as hgnc_id, o.id as mgi_id, rh.publications as reference, mp.id as MP_id, mp.name as MP_name, hp.id as HP_id, hp.name as HP_name
        """, hgnc_ids=hgnc_ids)
        return res.data()


class GeneOrthologs(Tool):
    pass


got = GeneOrthologs(
    name="mouse_orthologs",
    description="Retrieves mouse orthologs genes and their phenotypes fpr a list of human genes. Use this tool when: "
                "(1) the query asks about animal models, "
                "(2) no human phenotypes evidence is found for candidate genes, "
                "(3) the query explicitly mentions mouse model or orthologs. "
                "Input: list of HGNC IDs from candidate genes in the case report. ",
    execute_func=phenotype_orthologs,
    parameters=ObjectParameter(
        description="Tool parameters",
        required=True,
        properties=dict(
            hgnc_ids=ArrayParameter(
                description="List of HGNC ids",
                required=True,
                items=StringParameter(
                    description="A single HGNC Gene ID"
                )
            )
        ),
        required_properties=["hgnc_ids"]
    )
)


# tool = Tool(name="Mouse Orthologs",
#             description="This rool should be used when no evidence in human has been found",
#             execute_func=phenotype_orthologs,
#             parameters={
#                 'hgnc_ids': "Human Gene identifiers HGNC:XXXX"
#             })


