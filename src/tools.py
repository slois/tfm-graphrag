from src.retrievers.context_retriever import t2c_context_retriever
from src.retrievers.factual_retriever import factual_retriever
from src.retrievers.multihop_retriever import multihop_t2c_retriever
from src.retrievers.phenotypic_similarity_retriever import rank_disease_retriever, rank_gene_retriever
from src.retrievers.vector_retriever import disease_vector_retriever



one_hop_tool = t2c_context_retriever.convert_to_tool(
    name="one-hop_graph_traversal",
    description="""
    Executes 1-hop graph traversals across the biomedical knowledge graph. "
        "Use for simple queries requiring 1+ relationship hops such as: "
        "(1) Gene→Disease: disease caused by a gene. "
        "(2) Gene→Phenotype: phenotypes associated to a gene. "
        "(3) Phenotype→Disease: diseases with given phenotypes. "
        "(4) Gene→Ortholog: Human-Mouse orthologos. "
        "(5) HumanPhenotype→MousePhenotype: Human-Mouse phenotype equivalences. "
        "(6) Case→Gene: clinical case gene association. "
        "(7) Case→Disease: clinical case disease association. "
        "(8) Case→Phenotype: clinical case phenotype description. "
        "(9) Ontology expansion: child or parents of a term via subclass_of. "
        "Use when the query requires direct connection between entities or ontology levels."
    """
)

multihop_tool = multihop_t2c_retriever.convert_to_tool(
    name="multihop_graph_traversal",
    description=(
        "Executes multi-hop graph traversals across the biomedical knowledge graph. "
        "Use for complex queries requiring 2+ relationship hops such as: "
        "(1) Gene→Disease→Phenotype: phenotypes of diseases caused by a gene. "
        "(2) Phenotype→Disease→Gene: genes implicated in diseases with given phenotypes. "
        "(3) Gene→Ortholog→MousePhenotype→HumanPhenotype: cross-species evidence. "
        "(4) Case→Gene→Disease→Phenotype: clinical case multi-hop context. "
        "(5) Ontology expansion: descendants/ancestors via subclass_of traversal. "
        "(6) Shortest path between any two entities in the graph. "
        "Use when the query requires connecting entities across multiple relationship types or ontology levels."
    )
)

factual_tool = factual_retriever.convert_to_tool(
    name="factual_lookup",
    description="Use this tool to retrieve internal properties, definitions, descriptions, or official metadata "
                "of a specific entity (`biolink:Gene`, `biolink:Disease`, `biolink:PhenotypicFeature`,...). This tool "
                "does NOT explore relationships or associations between entities. Use it when you need to know exactly "
                "what an entity is or what its specific attributes are: "
                "(1) What is the symbol of the gene with id HGNC:2348?"
                "(2) What is the description of the disease with id MONDO:0008393?"
                "(3) What synonyms does the phenotype with id HP:0001249 have?"
)

disease_vector_context_tool = disease_vector_retriever.convert_to_tool(
    name="disease_vector_context",
    description="""
    This tool should be used when the query is general in nature and about a disease. 
    """)

#     General-purpose tool to query the knowledge graph using natural language.
#     Translates the question into a Cypher query and retrieves structured data
#     directly from the graph.
#     Use this tool for ANY of the following scenarios:
    # (1) Gene-phenotype associations: phenotypes of a gene, genes associated
    # with specific HPO terms, publications supporting gene-phenotype links.
    # (2) Gene-disease relationships: diseases caused by a gene, genes causing
    # a disease, association type (causes, contributes_to, associated_with).
    # (3) Disease features: phenotypic profile of a disease, inheritance pattern,
    # causal genes, disease description, subtype hierarchy.
    # (4) Variant information: sequence variants reported for a gene, variants
    # associated with a disease, variant-gene-disease relationships.
    # (5) Clinical cases: cases with specific phenotypes or genes, frequency of
    # gene-phenotype co-occurrence in reported cases.
    # (6) Ontology traversal: ancestor/descendant terms in HPO or MONDO,
    # phenotype similarity via shared ontology structure.
    # (7) Comparative queries: rank genes by phenotype overlap, diseases sharing
    # "phenotypes with a patient profile, differential diagnosis.
    # (8) Pathway and functional context: biological processes, molecular
    # activities or pathways associated with candidate genes.

disease_context_tool = disease_vector_retriever.convert_to_tool(
    name="disease_phenotype_context_tool",
    description="This tool allows you to search for diseases based on semantic similarity and generates context based "
                "on the diseases associated with it.",
    parameter_descriptions={'top_k': 'Number of items retrieved in vector search'}
)

disease_similarity_tool = rank_disease_retriever.convert_to_tool(
    name="rank_diseases",
    description="This tool allows you to rank diseases according to Resnik’s semantic similarity. "
                "This is particularly useful when a user’s query suggests a ranking based on phenotypic similarity or "
                "some form of disease prioritisation."
)

gene_similarity_tool = rank_gene_retriever.convert_to_tool(
    name="rank_genes",
    description="This tool allows you to rank genes according to Resnik’s semantic similarity. "
                "This is particularly useful when a user’s query suggests a ranking based on phenotypic similarity or "
                "some form of gene prioritisation."
)

