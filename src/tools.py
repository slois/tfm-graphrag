from src.retrievers.vector_retriever import disease_retriever

disease_context_tool = disease_retriever.convert_to_tool(
    name="disease_phenotype_context",
    description="This tool allows you to search for diseases based on semantic similarity and generates context based "
                "on the diseases associated with it.",
    parameter_descriptions={'top_k': 'Number of items retrieved in vector search'}
)