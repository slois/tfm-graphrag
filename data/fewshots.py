FACTUAL_EXAMPLES = [
    "USER INPUT: What is the symbol of the gene with id HGNC:2348?"
    "CYPHER: "
    "MATCH (g:`biolink:Gene`)"
    "WHERE g.id = 'HGNC:2348'"
    "RETURN g.symbol",
    "USER INPUT: What is the description of the disease with id MONDO:0008393?"
    "CYPHER: "
    "MATCH (d:`biolink:Disease` {id: 'MONDO:0008393'}) RETURN d.description",
    "USER INPUT: What synonyms does the phenotype with id HP:0001249 have?"
    "CYPHER: "
    "MATCH (p:`biolink:PhenotypicFeature` {id: 'HP:0001249'}) RETURN p.synonym",
]


MULTIHOP_EXAMPLES = [

    # ── 2 saltos: Gen → Enfermedad → Fenotipo ─────────────────────────────────
    "USER INPUT: 'What phenotypes are linked with diseases caused by CREBBP?' "
    "CYPHER: "
    "MATCH (g:`biolink:Gene` {symbol: 'CREBBP', in_taxon: 'NCBITaxon:9606'}) "
    "-[:`biolink:causes`|`biolink:gene_associated_with_condition`]->(d:`biolink:Disease`) "
    "-[:`biolink:has_phenotype`]->(p:`biolink:PhenotypicFeature`) "
    "WHERE p.namespace = 'HP' "
    "RETURN DISTINCT g.symbol AS gene, d.name AS disease, "
    "p.id AS hpo_id, p.name AS phenotype "
    "ORDER BY d.name, p.name LIMIT 50",

    # ── 2 saltos: Fenotipo → Enfermedad → Gen ─────────────────────────────────
    "USER INPUT: 'What genes are associated with diseases that include "
    "broad thumbs HP:0001525 and intellectual disability HP:0001249?' "
    "CYPHER: "
    "MATCH (d:`biolink:Disease`)-[:`biolink:has_phenotype`]->"
    "(p1:`biolink:PhenotypicFeature` {id: 'HP:0001525'}) "
    "MATCH (d)-[:`biolink:has_phenotype`]->"
    "(p2:`biolink:PhenotypicFeature` {id: 'HP:0001249'}) "
    "MATCH (g:`biolink:Gene` {in_taxon: 'NCBITaxon:9606'})"
    "-[:`biolink:gene_associated_with_condition`]->(d) "
    "RETURN DISTINCT g.id AS gene_id, g.symbol AS symbol, "
    "d.name AS disease, d.id AS disease_id "
    "ORDER BY symbol LIMIT 50",

    # ── 3 saltos: Gen → Ortólogo → Fenotipo murino → Fenotipo humano ──────────
    "USER INPUT: 'What human phenotypes are equivalent to mouse phenotypes "
    "of SCN2A orthologs?' "
    "CYPHER: "
    "MATCH (g:`biolink:Gene` {symbol: 'SCN2A', in_taxon: 'NCBITaxon:9606'}) "
    "-[:`biolink:orthologous_to`]->(mg:`biolink:Gene` {in_taxon: 'NCBITaxon:10090'}) "
    "-[:`biolink:has_phenotype`]->(mp:`biolink:PhenotypicFeature` {namespace: 'MP'}) "
    "-[:`biolink:same_as`|`biolink:homologous_to`]->(hp:`biolink:PhenotypicFeature` {namespace: 'HP'}) "
    "RETURN DISTINCT g.symbol AS human_gene, mg.name AS mouse_ortholog, "
    "mp.name AS mouse_phenotype, hp.id AS hpo_id, hp.name AS human_phenotype "
    "LIMIT 50",

    # ── 3 saltos: Caso → Gen → Enfermedad → Fenotipo ──────────────────────────
    "USER INPUT: 'What phenotypes characterize diseases in cases where "
    "ANKRD11 is the implicated gene?' "
    "CYPHER: "
    "MATCH (c:`biolink:Case`)-[:`biolink:has_gene`]->"
    "(g:`biolink:Gene` {id: 'HGNC:21316'}) "
    "MATCH (c)-[:`biolink:has_disease`]->(d:`biolink:Disease`) "
    "MATCH (d)-[:`biolink:has_phenotype`]->(p:`biolink:PhenotypicFeature`) "
    "WHERE p.namespace = 'HP' "
    "RETURN DISTINCT g.symbol AS gene, d.name AS disease, "
    "p.id AS hpo_id, p.name AS phenotype, "
    "count(DISTINCT c) AS n_cases "
    "ORDER BY n_cases DESC LIMIT 50",

    # ── Multi-hop con expansión ontológica ─────────────────────────────────────
    "USER INPUT: 'Which genes are associated with phenotypes that are "
    "descendants of seizures HP:0001250 including more specific terms?' "
    "CYPHER: "
    "MATCH (query_term:`biolink:PhenotypicFeature` {id: 'HP:0001250'}) "
    "MATCH (specific_pheno:`biolink:PhenotypicFeature`)"
    "-[:`biolink:subclass_of`*0..]->(query_term) "
    "WHERE specific_pheno.namespace = 'HP' "
    "MATCH (g:`biolink:Gene` {in_taxon: 'NCBITaxon:9606'})"
    "-[:`biolink:has_phenotype`]->(specific_pheno) "
    "WITH g, count(DISTINCT specific_pheno) AS n_seizure_phenotypes "
    "RETURN g.id AS gene_id, g.symbol AS symbol, n_seizure_phenotypes "
    "ORDER BY n_seizure_phenotypes DESC LIMIT 20",

    # ── Camino más corto entre entidades ──────────────────────────────────────
    "USER INPUT: 'Find shortest path between CREBBP HGNC:2348 "
    "and microcephaly HP:0000252' "
    "CYPHER: "
    "MATCH (g:`biolink:Gene` {id: 'HGNC:2348'}) "
    "MATCH (p:`biolink:PhenotypicFeature` {id: 'HP:0000252'}) "
    "MATCH path = shortestPath((g)-[*..6]-(p)) "
    "RETURN [n IN nodes(path) | {id: n.id, name: n.name, label: labels(n)[0]}] "
    "AS path_nodes, "
    "[r IN relationships(path) | type(r)] AS path_relationships, "
    "length(path) AS hops "
    "LIMIT 5",

    # ── 2 saltos: Variante → Gen → Fenotipo ───────────────────────────────────
    "USER INPUT: 'What phenotypes are associated with genes that have "
    "sequence variants in cases with intellectual disability HP:0001249?' "
    "CYPHER: "
    "MATCH (c:`biolink:Case`)-[:`biolink:has_phenotype`]->"
    "(p_case:`biolink:PhenotypicFeature` {id: 'HP:0001249'}) "
    "MATCH (c)-[:`biolink:has_gene`]->(g:`biolink:Gene` {in_taxon: 'NCBITaxon:9606'}) "
    "MATCH (g)-[:`biolink:has_phenotype`]->(p_gene:`biolink:PhenotypicFeature`) "
    "WHERE p_gene.namespace = 'HP' "
    "RETURN DISTINCT g.symbol AS gene, "
    "p_gene.id AS hpo_id, p_gene.name AS phenotype, "
    "count(DISTINCT c) AS n_cases "
    "ORDER BY n_cases DESC LIMIT 30",
]

NEIGHBORHOOD_EXAMPLES = [
    # Gene context
    "USER INPUT: 'Context of gene SCN2A [HGNC:10588]' "
    "CYPHER: MATCH (g:`biolink:Gene` {id: 'HGNC:10588'}) "
    "OPTIONAL MATCH (g)-[:`biolink:has_phenotype`]->(p:`biolink:PhenotypicFeature`) WHERE p.namespace='HP' "
    "OPTIONAL MATCH (g)-[:`biolink:causes`|`biolink:gene_associated_with_condition`]->(d:`biolink:Disease`) "
    "OPTIONAL MATCH (sv:`biolink:SequenceVariant`)-[:`biolink:is_sequence_variant_of`]->(g) "
    "RETURN g.id AS entity_id, g.name AS entity_name, 'Gene' AS entity_type, "
    "g.full_name AS full_name, "
    "collect(DISTINCT p.name+' ('+p.id+')')[..10] AS phenotypes, "
    "collect(DISTINCT d.name+' ('+d.id+')')[..10] AS diseases, "
    "collect(DISTINCT sv.id)[..5] AS variants",

    # Disease context
    "USER INPUT: 'Context of disease Kabuki syndrome [MONDO:0016512]' "
    "CYPHER: MATCH (d:`biolink:Disease` {id: 'MONDO:0016512'}) "
    "OPTIONAL MATCH (d)-[:`biolink:has_phenotype`]->(p:`biolink:PhenotypicFeature`) WHERE p.namespace='HP' "
    "OPTIONAL MATCH (g:`biolink:Gene` {in_taxon:'NCBITaxon:9606'})-[:`biolink:causes`|`biolink:gene_associated_with_condition`]->(d) "
    "OPTIONAL MATCH (d)-[:`biolink:has_mode_of_inheritance`]->(inh:`biolink:PhenotypicFeature`) "
    "RETURN d.id AS entity_id, d.name AS entity_name, 'Disease' AS entity_type, "
    "d.description AS description, "
    "collect(DISTINCT p.name+' ('+p.id+')')[..15] AS phenotypes, "
    "collect(DISTINCT g.symbol+' ('+g.id+')') AS causal_genes, "
    "collect(DISTINCT inh.name) AS inheritance",

    # PhenotypicFeature context
    "USER INPUT: 'Context of phenotype intellectual disability [HP:0001249]' "
    "CYPHER: MATCH (p:`biolink:PhenotypicFeature` {id: 'HP:0001249'}) "
    "OPTIONAL MATCH (p)-[:`biolink:subclass_of`*1..2]->(anc:`biolink:PhenotypicFeature`) WHERE anc.namespace='HP' "
    "OPTIONAL MATCH (p)<-[:`biolink:subclass_of`]-(child:`biolink:PhenotypicFeature`) WHERE child.namespace='HP' "
    "OPTIONAL MATCH (d:`biolink:Disease`)-[:`biolink:has_phenotype`]->(p) "
    "RETURN p.id AS entity_id, p.name AS entity_name, 'PhenotypicFeature' AS entity_type, "
    "p.IC_disease AS ic, "
    "collect(DISTINCT anc.name+' ('+anc.id+')')[..5] AS ancestors, "
    "collect(DISTINCT child.name+' ('+child.id+')')[..5] AS children, "
    "collect(DISTINCT d.name+' ('+d.id+')')[..10] AS diseases_with_phenotype",

    # Multi-entity context
    "USER INPUT: 'Context of genes KCNQ2 [HGNC:6296] SCN1A [HGNC:10585]' "
    "CYPHER: MATCH (g:`biolink:Gene`) WHERE g.id IN ['HGNC:6296','HGNC:10585'] "
    "OPTIONAL MATCH (g)-[:`biolink:has_phenotype`]->(p:`biolink:PhenotypicFeature`) WHERE p.namespace='HP' "
    "OPTIONAL MATCH (g)-[:`biolink:causes`|`biolink:gene_associated_with_condition`]->(d:`biolink:Disease`) "
    "RETURN g.id AS entity_id, g.name AS entity_name, 'Gene' AS entity_type, "
    "g.symbol AS symbol, "
    "collect(DISTINCT p.name+' ('+p.id+')')[..10] AS phenotypes, "
    "collect(DISTINCT d.name+' ('+d.id+')')[..5] AS diseases",

    # SequenceVariant context
    "USER INPUT: 'Context of variant in ALDH7A1 [HGNC:408]' "
    "CYPHER: MATCH (g:`biolink:Gene` {id: 'HGNC:408'}) "
    "OPTIONAL MATCH (sv:`biolink:SequenceVariant`)-[:`biolink:is_sequence_variant_of`]->(g) "
    "OPTIONAL MATCH (g)-[:`biolink:causes`|`biolink:gene_associated_with_condition`]->(d:`biolink:Disease`) "
    "OPTIONAL MATCH (g)-[:`biolink:has_phenotype`]->(p:`biolink:PhenotypicFeature`) WHERE p.namespace='HP' "
    "RETURN g.id AS entity_id, g.name AS entity_name, 'Gene' AS entity_type, "
    "collect(DISTINCT sv.id+' ('+sv.name+')')[..10] AS variants, "
    "collect(DISTINCT d.name+' ('+d.id+')')[..5] AS diseases, "
    "collect(DISTINCT p.name+' ('+p.id+')')[..10] AS phenotypes",
]