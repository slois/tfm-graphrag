FACTUAL_SCHEMA = """
Node properties:
- `biolink:AnatomicalEntity` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, deprecated: BOOLEAN, iri: STRING, namespace: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, broad_synonym: LIST, related_synonym: LIST, subsets: STRING, narrow_synonym: LIST}
- `biolink:BiologicalProcess` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, synonym: LIST, exact_synonym: LIST, narrow_synonym: LIST, broad_synonym: LIST, subsets: STRING, related_synonym: LIST, in_taxon: STRING, xref: LIST}
- `biolink:Case` {id: STRING, category: LIST, name: STRING, provided_by: STRING, has_biological_sex: STRING, namespace: STRING}
- `biolink:Cell` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, related_synonym: LIST, iri: STRING, subsets: STRING, namespace: STRING, deprecated: BOOLEAN, broad_synonym: LIST, narrow_synonym: LIST}
- `biolink:CellularComponent` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, xref: LIST, synonym: LIST, narrow_synonym: LIST, related_synonym: LIST, exact_synonym: LIST, subsets: STRING, broad_synonym: LIST}
- `biolink:Disease` {id: STRING, category: LIST, name: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, related_synonym: LIST, iri: STRING, subsets: STRING, namespace: STRING, embedding: LIST, description: STRING, broad_synonym: LIST, narrow_synonym: LIST, deprecated: BOOLEAN}
- `biolink:Gene` {id: STRING, category: LIST, name: STRING, full_name: STRING, in_taxon: STRING, in_taxon_label: STRING, symbol: STRING, provided_by: STRING, type: STRING, xref: LIST, synonym: LIST, namespace: STRING}
- `biolink:Genotype` {id: STRING, category: LIST, name: STRING, in_taxon: STRING, in_taxon_label: STRING, provided_by: STRING, type: STRING, namespace: STRING}
- `biolink:MolecularActivity`  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, synonym: LIST, related_synonym: LIST, iri: STRING, namespace: STRING, exact_synonym: LIST, xref: LIST, broad_synonym: LIST, narrow_synonym: LIST, subsets: STRING}
- `biolink:Occurrent`  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, synonym: LIST, exact_synonym: LIST, narrow_synonym: LIST, xref: LIST, related_synonym: LIST, broad_synonym: LIST, subsets: STRING, in_taxon: STRING}
- `biolink:Pathway` {id: STRING, category: LIST, name: STRING, in_taxon: STRING, provided_by: STRING, namespace: STRING}
- `biolink:PhenotypicFeature` {IC_gene: FLOAT, Gene_freq: INTEGER, id: STRING, category: LIST, name: STRING, description: STRING, Disease_freq: INTEGER, provided_by: STRING, xref: LIST, iri: STRING, namespace: STRING, embedding: LIST, IC_disease: FLOAT, synonym: LIST, exact_synonym: LIST, subsets: STRING, broad_synonym: LIST, narrow_synonym: LIST, related_synonym: LIST}
- `biolink:Protein`  {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, iri: STRING, namespace: STRING, related_synonym: LIST, broad_synonym: LIST, narrow_synonym: LIST}
- `biolink:SequenceVariant` {id: STRING, category: LIST, name: STRING, in_taxon: STRING, in_taxon_label: STRING, provided_by: STRING, xref: LIST, has_gene: LIST, namespace: STRING, type: STRING}

CRITICAL RULES:
- NO RELATIONSHIPS: Do not use patterns like (n)-[r]-(m). Only use single node patterns: (n:Label).
- PROPERTY EXTRACTION: Use RETURN n.* or specify all relevant properties such as id, name, description, symbol, full_name, synonyms, and IRI.
- TAXON FILTER: If the entity is a `biolink:Gene`, apply the filter n.in_taxon = 'NCBITaxon:9606' for human or 'NCBITaxon:10090' for mouse if specified.
- Please provide ONLY the requested information; DO NOT include evidences or triples details in your response
"""



NEO4J_SCHEMA = """
Node types:
- `biolink:AnatomicalEntity` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, deprecated: BOOLEAN, iri: STRING, namespace: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, broad_synonym: LIST, related_synonym: LIST, subsets: STRING, narrow_synonym: LIST}
- `biolink:BiologicalProcess` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, synonym: LIST, exact_synonym: LIST, narrow_synonym: LIST, broad_synonym: LIST, subsets: STRING, related_synonym: LIST, in_taxon: STRING, xref: LIST}
- `biolink:Case` {id: STRING, category: LIST, name: STRING, provided_by: STRING, has_biological_sex: STRING, namespace: STRING}
- `biolink:Cell` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, related_synonym: LIST, iri: STRING, subsets: STRING, namespace: STRING, deprecated: BOOLEAN, broad_synonym: LIST, narrow_synonym: LIST}
- `biolink:CellularComponent` {id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, xref: LIST, synonym: LIST, narrow_synonym: LIST, related_synonym: LIST, exact_synonym: LIST, subsets: STRING, broad_synonym: LIST}
- `biolink:Disease` {id: STRING, category: LIST, name: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, related_synonym: LIST, iri: STRING, subsets: STRING, namespace: STRING, embedding: LIST, description: STRING, broad_synonym: LIST, narrow_synonym: LIST, deprecated: BOOLEAN}
- `biolink:Gene` {id: STRING, category: LIST, name: STRING, full_name: STRING, in_taxon: STRING, in_taxon_label: STRING, symbol: STRING, provided_by: STRING, type: STRING, xref: LIST, synonym: LIST, namespace: STRING}
- `biolink:Genotype` {id: STRING, category: LIST, name: STRING, in_taxon: STRING, in_taxon_label: STRING, provided_by: STRING, type: STRING, namespace: STRING}
- `biolink:Pathway` {id: STRING, category: LIST, name: STRING, in_taxon: STRING, provided_by: STRING, namespace: STRING}
- `biolink:PhenotypicFeature` {IC_gene: FLOAT, Gene_freq: INTEGER, id: STRING, category: LIST, name: STRING, description: STRING, Disease_freq: INTEGER, provided_by: STRING, xref: LIST, iri: STRING, namespace: STRING, IC_disease: FLOAT, synonym: LIST, exact_synonym: LIST, subsets: STRING, broad_synonym: LIST, narrow_synonym: LIST, related_synonym: LIST}
- `biolink:SequenceVariant` {id: STRING, category: LIST, name: STRING, in_taxon: STRING, in_taxon_label: STRING, provided_by: STRING, xref: LIST, has_gene: LIST, namespace: STRING, type: STRING}


Relationships (use backticks for ALL):
- `biolink:Gene`-[`biolink:causes`]-> `biolink:Disease`
- `biolink:Gene`-[`biolink:gene_associated_with_condition`]-> `biolink:Disease`
- `biolink:Gene`-[`biolink:contributes_to`]-> `biolink:Disease`
- `biolink:Gene`-[`biolink:genetically_associated_with`]-> `biolink:Disease`
- `biolink:Gene`-[`biolink:has_phenotype`]-> `biolink:PhenotypicFeature`
- `biolink:Gene`-[`biolink:orthologous_to`]-> `biolink:Gene`
- `biolink:Gene`-[`biolink:interacts_with]-> `biolink:Gene`
- `biolink:Gene`-[`biolink:participates_in`]-> `biolink:Pathway`
- `biolink:Gene`-[`biolink:actively_involved_in`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:acts_upstream_of_or_within`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:acts_upstream_of_or_within_positive_effect`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:acts_upstream_of`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:acts_upstream_of_or_within_negative_effect`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:participates_in`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:acts_upstream_of_negative_effect`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:acts_upstream_of_positive_effect`]-> `biolink:BiologicalProcess`
- `biolink:Gene`-[`biolink:expressed_in]-> `biolink:AnatomicalEntity`    
- `biolink:Genotype`-[`biolink:has_phenotype`]-> `biolink:PhenotypicFeature`
- `biolink:Genotype`-[`biolink:has_sequence_variant`]-> `biolink:SequenceVariant`
- `biolink:Genotype`-[`biolink:model_of`]-> `biolink:Disease`
- `biolink:PhenotypicFeature`-[`biolink:subclass_of`]-> `biolink:PhenotypicFeature`
- `biolink:PhenotypicFeature`-[`biolink:same_as`]-> `biolink:PhenotypicFeature`
- `biolink:PhenotypicFeature`-[`biolink:homologous_to`]-> `biolink:PhenotypicFeature`
- `biolink:Disease`-[`biolink:has_mode_of_inheritance`]-> `biolink:PhenotypicFeature`
- `biolink:Disease`-[`biolink:has_phenotype`]-> `biolink:PhenotypicFeature`
- `biolink:Disease`-[`biolink:disease_has_location`]-> `biolink:AnatomicalEntity`
- `biolink:Disease`-[`biolink:subclass_of`]-> `biolink:Disease`
- `biolink:Disease`-[`biolink:has_participant`]-> `biolink:BiologicalProcess`
- `biolink:Disease`-[`biolink:disrupts`]-> `biolink:BiologicalProcess`
- `biolink:Disease`-[`biolink:has_participant`]->:biolink:AnatomicalEntity
- `biolink:SequenceVariant`-[`biolink:is_sequence_variant_of`]-> `biolink:Gene`
- `biolink:SequenceVariant`-[`biolink:has_phenotype`] -> `biolink:PhenotypicFeature`
- `biolink:SequenceVariant`-[`biolink:contributes_to`] -> `biolink:PhenotypicFeature`
- `biolink:SequenceVariant`-[`biolink:causes`] -> `biolink:Disease`
- `biolink:SequenceVariant`-[`biolink:associated_with_increased_likelihood_of`] -> `biolink:Disease`
- `biolink:SequenceVariant`-[`biolink:genetically_associated_with`] -> `biolink:Disease`
- `biolink:Case`-[`biolink:has_gene`]-> `biolink:Gene`
- `biolink:Case`-[`biolink:has_disease`]-> `biolink:Disease`
- `biolink:Case`-[`biolink:has_phenotype`]-> `biolink:PhenotypicFeature`
"""

EXTENDED_NEO4J_SCHEMA="""
Node properties:
biolink:Gene {id: STRING, category: LIST, name: STRING, full_name: STRING, in_taxon: STRING, in_taxon_label: STRING, symbol: STRING, provided_by: STRING, type: STRING, xref: LIST, synonym: LIST, namespace: STRING}
NTEGER, IC_disease: FLOAT, Disease_freq: INTEGER, xref: LIST, embedding: LIST, in_taxon: STRING, in_taxon_label: STRING, full_name: STRING, symbol: STRING, related_synonym: LIST, deprecated: BOOLEAN, has_gene: LIST, narrow_synonym: LIST}
biolink:SequenceVariant {id: STRING, category: LIST, name: STRING, in_taxon: STRING, in_taxon_label: STRING, provided_by: STRING, xref: LIST, has_gene: LIST, namespace: STRING, type: STRING}
biolink:PhenotypicFeature {IC_gene: FLOAT, Gene_freq: INTEGER, id: STRING, category: LIST, name: STRING, description: STRING, Disease_freq: INTEGER, provided_by: STRING, xref: LIST, iri: STRING, namespace: STRING, embedding: LIST, IC_disease: FLOAT, synonym: LIST, exact_synonym: LIST, subsets: STRING, broad_synonym: LIST, narrow_synonym: LIST, related_synonym: LIST}
biolink:Disease {id: STRING, category: LIST, name: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, related_synonym: LIST, iri: STRING, subsets: STRING, namespace: STRING, embedding: LIST, description: STRING, broad_synonym: LIST, narrow_synonym: LIST, deprecated: BOOLEAN}
biolink:Genotype {id: STRING, category: LIST, name: STRING, in_taxon: STRING, in_taxon_label: STRING, provided_by: STRING, type: STRING, namespace: STRING}
biolink:AnatomicalEntity  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, deprecated: BOOLEAN, iri: STRING, namespace: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, broad_synonym: LIST, related_synonym: LIST, subsets: STRING, narrow_synonym: LIST}
biolink:Cell  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, related_synonym: LIST, iri: STRING, subsets: STRING, namespace: STRING, deprecated: BOOLEAN, broad_synonym: LIST, narrow_synonym: LIST}
biolink:Protein  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, xref: LIST, synonym: LIST, exact_synonym: LIST, iri: STRING, namespace: STRING, related_synonym: LIST, broad_synonym: LIST, narrow_synonym: LIST}
biolink:Case  id: STRING, category: LIST, name: STRING, provided_by: STRING, has_biological_sex: STRING, namespace: STRING}
biolink:BiologicalProcessOrActivity  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, synonym: LIST, exact_synonym: LIST, iri: STRING, namespace: STRING, related_synonym: LIST, narrow_synonym: LIST, xref: LIST, broad_synonym: LIST, subsets: STRING, in_taxon: STRING}
biolink:BiologicalProcess  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, synonym: LIST, exact_synonym: LIST, narrow_synonym: LIST, broad_synonym: LIST, subsets: STRING, related_synonym: LIST, in_taxon: STRING, xref: LIST}
biolink:MolecularActivity  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, synonym: LIST, related_synonym: LIST, iri: STRING, namespace: STRING, exact_synonym: LIST, xref: LIST, broad_synonym: LIST, narrow_synonym: LIST, subsets: STRING}
biolink:CellularComponent  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, xref: LIST, synonym: LIST, narrow_synonym: LIST, related_synonym: LIST, exact_synonym: LIST, subsets: STRING, broad_synonym: LIST}
biolink:Pathway {id: STRING, category: LIST, name: STRING, in_taxon: STRING, provided_by: STRING, namespace: STRING}
biolink:Occurrent  id: STRING, category: LIST, name: STRING, description: STRING, provided_by: STRING, iri: STRING, namespace: STRING, synonym: LIST, exact_synonym: LIST, narrow_synonym: LIST, xref: LIST, related_synonym: LIST, broad_synonym: LIST, subsets: STRING, in_taxon: STRING}

Relationship properties:
biolink:interacts_with {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, has_evidence: LIST, subject: STRING, object: STRING, original_subject: STRING, original_object: STRING, publications: LIST, exclude_reason: STRING, negated: BOOLEAN, species_context_qualifier: STRING}
biolink:located_in {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:expressed_in {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, qualifiers: LIST, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING, object_specialization_qualifier: STRING}
biolink:enables {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:has_phenotype {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, subject: STRING, object: STRING, disease_context_qualifier: STRING, has_count: INTEGER, has_percentage: STRING, has_quotient: STRING, has_total: INTEGER, original_subject: STRING, frequency_qualifier: STRING, exclude_reason: STRING, negated: BOOLEAN, onset_qualifier: STRING, has_evidence: LIST, sex_qualifier: STRING}
biolink:part_of {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:acts_upstream_of_or_within {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:actively_involved_in {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:is_active_in {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:contributes_to {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, original_object: STRING}
biolink:colocalizes_with {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:orthologous_to {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, has_evidence: LIST, subject: STRING, object: STRING, exclude_reason: STRING}
biolink:acts_upstream_of_or_within_positive_effect {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING}
biolink:acts_upstream_of_positive_effect {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING}
biolink:acts_upstream_of {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING}
biolink:acts_upstream_of_or_within_negative_effect {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING}
biolink:acts_upstream_of_negative_effect {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, negated: BOOLEAN, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, species_context_qualifier: STRING, subject: STRING, object: STRING, original_subject: STRING}
biolink:related_to {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING}
biolink:subclass_of  id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING}
biolink:model_of {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, subject: STRING, object: STRING, original_object: STRING,
biolink:has_disease {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, subject: STRING, object: STRING, original_object: STRING, onset_qualifier: STRING}
biolink:has_gene {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, subject: STRING, object: STRING}
biolink:is_sequence_variant_of {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING, original_object: STRING, exclude_reason: STRING, original_predicate: STRING}
biolink:same_as  id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING}
biolink:homologous_to {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, knowledge_level: STRING, original_predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING, object_category: STRING, subject_category: STRING, has_attribute: LIST, knowledge_source: STRING, subject: STRING, object: STRING}
biolink:causes {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, knowledge_level: STRING, provided_by: STRING, subject: STRING, object: STRING, original_subject: STRING, original_object: STRING, aggregator_knowledge_source: LIST, original_predicate: STRING, primary_knowledge_source: STRING, qualifiers: LIST, exclude_reason: STRING}
biolink:associated_with_increased_likelihood_of {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, original_predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING, qualifiers: LIST, exclude_reason: STRING}
biolink:has_mode_of_inheritance {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, publications: LIST, has_evidence: LIST, subject: STRING, object: STRING, original_subject: STRING}
biolink:has_participant {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING,
biolink:disrupts {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING,
biolink:disease_has_location {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING}
biolink:participates_in {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING, original_subject: STRING, exclude_reason: STRING}
biolink:has_sequence_variant {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, qualifier: STRING, subject: STRING, object: STRING}
biolink:genetically_associated_with {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, original_predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING}
biolink:gene_associated_with_condition {id: STRING, predicate: STRING, category: LIST, agent_type: STRING, aggregator_knowledge_source: LIST, knowledge_level: STRING, primary_knowledge_source: STRING, provided_by: STRING, subject: STRING, object: STRING, original_subject: STRING, original_object: STRING, exclude_reason: STRING}

The relationships:
(:biolink:Gene)-[:biolink:interacts_with]->(:biolink:Gene)
(:biolink:Gene)-[:biolink:located_in]->(:biolink:AnatomicalEntity)
(:biolink:Gene)-[:biolink:located_in]->(:biolink:CellularComponent)
(:biolink:Gene)-[:biolink:participates_in]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:participates_in]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:participates_in]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:participates_in]->(:biolink:Pathway)
(:biolink:Gene)-[:biolink:expressed_in]->(:biolink:AnatomicalEntity)
(:biolink:Gene)-[:biolink:expressed_in]->(:biolink:Cell)
(:biolink:Gene)-[:biolink:enables]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:enables]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:enables]->(:biolink:MolecularActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:actively_involved_in]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:actively_involved_in]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:actively_involved_in]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:is_active_in]->(:biolink:AnatomicalEntity)
(:biolink:Gene)-[:biolink:is_active_in]->(:biolink:CellularComponent)
(:biolink:Gene)-[:biolink:orthologous_to]->(:biolink:Gene)
(:biolink:Gene)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:Gene)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Gene)-[:biolink:part_of]->(:biolink:AnatomicalEntity)
(:biolink:Gene)-[:biolink:part_of]->(:biolink:CellularComponent)
(:biolink:Gene)-[:biolink:contributes_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:contributes_to]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:contributes_to]->(:biolink:MolecularActivity)
(:biolink:Gene)-[:biolink:colocalizes_with]->(:biolink:AnatomicalEntity)
(:biolink:Gene)-[:biolink:colocalizes_with]->(:biolink:CellularComponent)
(:biolink:Gene)-[:biolink:gene_associated_with_condition]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Gene)-[:biolink:gene_associated_with_condition]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:causes]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Gene)-[:biolink:causes]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:acts_upstream_of]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:acts_upstream_of]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within_positive_effect]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within_positive_effect]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within_positive_effect]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:acts_upstream_of_negative_effect]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of_negative_effect]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:acts_upstream_of_negative_effect]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within_negative_effect]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within_negative_effect]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:acts_upstream_of_or_within_negative_effect]->(:biolink:Occurrent)
(:biolink:Gene)-[:biolink:acts_upstream_of_positive_effect]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Gene)-[:biolink:acts_upstream_of_positive_effect]->(:biolink:BiologicalProcess)
(:biolink:Gene)-[:biolink:acts_upstream_of_positive_effect]->(:biolink:Occurrent)
(:biolink:SequenceVariant)-[:biolink:is_sequence_variant_of]->(:biolink:Gene)
(:biolink:SequenceVariant)-[:biolink:causes]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:SequenceVariant)-[:biolink:causes]->(:biolink:Disease)
(:biolink:SequenceVariant)-[:biolink:associated_with_increased_likelihood_of]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:SequenceVariant)-[:biolink:associated_with_increased_likelihood_of]->(:biolink:Disease)
(:biolink:SequenceVariant)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:SequenceVariant)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:SequenceVariant)-[:biolink:genetically_associated_with]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:SequenceVariant)-[:biolink:genetically_associated_with]->(:biolink:Disease)
(:biolink:PhenotypicFeature)-[:biolink:subclass_of]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:subclass_of]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:subclass_of]->(:biolink:AnatomicalEntity)
(:biolink:PhenotypicFeature)-[:biolink:homologous_to]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:homologous_to]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:same_as]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:same_as]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:subclass_of]->(:biolink:PhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:subclass_of]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:subclass_of]->(:biolink:Disease)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:subclass_of]->(:biolink:AnatomicalEntity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:homologous_to]->(:biolink:PhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:homologous_to]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:same_as]->(:biolink:PhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:same_as]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:Disease)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:related_to]->(:biolink:PhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_mode_of_inheritance]->(:biolink:PhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_mode_of_inheritance]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:disease_has_location]->(:biolink:AnatomicalEntity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_participant]->(:biolink:BiologicalProcessOrActivity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_participant]->(:biolink:Occurrent)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_participant]->(:biolink:MolecularActivity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:has_participant]->(:biolink:BiologicalProcess)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:disrupts]->(:biolink:BiologicalProcessOrActivity)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:disrupts]->(:biolink:BiologicalProcess)
(:biolink:DiseaseOrPhenotypicFeature)-[:biolink:disrupts]->(:biolink:Occurrent)
(:biolink:Disease)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:Disease)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Disease)-[:biolink:subclass_of]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Disease)-[:biolink:subclass_of]->(:biolink:Disease)
(:biolink:Disease)-[:biolink:has_mode_of_inheritance]->(:biolink:PhenotypicFeature)
(:biolink:Disease)-[:biolink:has_mode_of_inheritance]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:Disease)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:Disease)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:Disease)-[:biolink:disease_has_location]->(:biolink:AnatomicalEntity)
(:biolink:Disease)-[:biolink:disease_has_location]->(:biolink:CellularComponent)
(:biolink:Disease)-[:biolink:has_participant]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Disease)-[:biolink:has_participant]->(:biolink:BiologicalProcess)
(:biolink:Disease)-[:biolink:has_participant]->(:biolink:Occurrent)
(:biolink:Disease)-[:biolink:has_participant]->(:biolink:AnatomicalEntity)
(:biolink:Disease)-[:biolink:has_participant]->(:biolink:CellularComponent)
(:biolink:Disease)-[:biolink:has_participant]->(:biolink:MolecularActivity)
(:biolink:Disease)-[:biolink:disrupts]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Disease)-[:biolink:disrupts]->(:biolink:BiologicalProcess)
(:biolink:Disease)-[:biolink:disrupts]->(:biolink:Occurrent)
(:biolink:Genotype)-[:biolink:related_to]->(:biolink:SequenceVariant)
(:biolink:Genotype)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:Genotype)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Genotype)-[:biolink:has_sequence_variant]->(:biolink:SequenceVariant)
(:biolink:Genotype)-[:biolink:model_of]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Genotype)-[:biolink:model_of]->(:biolink:Disease)
(:biolink:AnatomicalEntity)-[:biolink:subclass_of]->(:biolink:AnatomicalEntity)
(:biolink:AnatomicalEntity)-[:biolink:subclass_of]->(:biolink:Cell)
(:biolink:AnatomicalEntity)-[:biolink:subclass_of]->(:biolink:CellularComponent)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:AnatomicalEntity)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:Cell)-[:biolink:subclass_of]->(:biolink:AnatomicalEntity)
(:biolink:Cell)-[:biolink:subclass_of]->(:biolink:Cell)
(:biolink:Cell)-[:biolink:subclass_of]->(:biolink:CellularComponent)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:Cell)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:Protein)-[:biolink:subclass_of]->(:biolink:Protein)
(:biolink:Protein)-[:biolink:subclass_of]->(:biolink:AnatomicalEntity)
(:biolink:Protein)-[:biolink:subclass_of]->(:biolink:CellularComponent)
(:biolink:Protein)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Protein)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:Protein)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:Protein)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:Protein)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:IndividualOrganism)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:IndividualOrganism)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:IndividualOrganism)-[:biolink:has_disease]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:IndividualOrganism)-[:biolink:has_disease]->(:biolink:Disease)
(:biolink:IndividualOrganism)-[:biolink:has_disease]->(:biolink:Gene)
(:biolink:IndividualOrganism)-[:biolink:has_gene]->(:biolink:Gene)
(:biolink:Case)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:Case)-[:biolink:has_phenotype]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Case)-[:biolink:has_disease]->(:biolink:DiseaseOrPhenotypicFeature)
(:biolink:Case)-[:biolink:has_disease]->(:biolink:Disease)
(:biolink:Case)-[:biolink:has_disease]->(:biolink:Gene)
(:biolink:Case)-[:biolink:has_gene]->(:biolink:Gene)
(:biolink:BiologicalProcessOrActivity)-[:biolink:subclass_of]->(:biolink:BiologicalProcessOrActivity)
(:biolink:BiologicalProcessOrActivity)-[:biolink:subclass_of]->(:biolink:Occurrent)
(:biolink:BiologicalProcessOrActivity)-[:biolink:subclass_of]->(:biolink:MolecularActivity)
(:biolink:BiologicalProcessOrActivity)-[:biolink:subclass_of]->(:biolink:BiologicalProcess)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:BiologicalProcessOrActivity)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:BiologicalProcess)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:BiologicalProcess)-[:biolink:subclass_of]->(:biolink:BiologicalProcessOrActivity)
(:biolink:BiologicalProcess)-[:biolink:subclass_of]->(:biolink:BiologicalProcess)
(:biolink:BiologicalProcess)-[:biolink:subclass_of]->(:biolink:Occurrent)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:Occurrent)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:Occurrent)-[:biolink:subclass_of]->(:biolink:BiologicalProcessOrActivity)
(:biolink:Occurrent)-[:biolink:subclass_of]->(:biolink:BiologicalProcess)
(:biolink:Occurrent)-[:biolink:subclass_of]->(:biolink:Occurrent)
(:biolink:Occurrent)-[:biolink:subclass_of]->(:biolink:MolecularActivity)
(:biolink:MolecularActivity)-[:biolink:subclass_of]->(:biolink:BiologicalProcessOrActivity)
(:biolink:MolecularActivity)-[:biolink:subclass_of]->(:biolink:Occurrent)
(:biolink:MolecularActivity)-[:biolink:subclass_of]->(:biolink:MolecularActivity)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:MolecularActivity)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:AnatomicalEntity)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:CellularComponent)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:BiologicalProcessOrActivity)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:Occurrent)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:MolecularActivity)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:Cell)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:BiologicalProcess)
(:biolink:CellularComponent)-[:biolink:related_to]->(:biolink:Protein)
(:biolink:CellularComponent)-[:biolink:subclass_of]->(:biolink:AnatomicalEntity)
(:biolink:CellularComponent)-[:biolink:subclass_of]->(:biolink:CellularComponent)
"""


GENERIC_NEO4J_SCHEMA="""
Node properties:
- biolink:BiologicalProcess {id: STRING, name: STRING}
- biolink:CellularComponent {id: STRING, name: STRING}
- biolink:Disease {id: STRING, name: STRING, description: STRING, iri: STRING}
- biolink:Gene {id: string, symbol: STRING, name: STRING, in_taxon: STRING, full_name: STRING}
- biolink:Genotype {id: string, name: string, in_taxon: STRING}
- biolink:MolecularActivity {id: STRING, name: STRING}
- biolink:OntologyClass {id: STRING, name: STRING}
- biolink:PhenotypicFeature {id: STRING, name: STRING, IC_disease: FLOAT, IC_gene: FLOAT, namespace: STRING, publications: LIST, synonym: LIST, exact_synonym: LIST}
- biolink:Pathway {id: STRING, name: STRING}
- biolink:SequenceVariant {id: STRING, name: STRING}

Relationship properties:
- biolink:actively_involved_in {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:acts_upstream_of {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:acts_upstream_of_negative_effect {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:acts_upstream_of_or_within {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:acts_upstream_of_or_within_negative_effect {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:acts_upstream_of_or_within_positive_effect {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:acts_upstream_of_positive_effect {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:associated_with_increased_likelihood_of {predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING}
- biolink:causes {predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING}
- biolink:contributes_to {predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING}
- biolink:disease_has_location {predicate: STRING, publications: LIST, primary_knowledge_source: STRING}
- biolink:disrupts {predicate: STRING, primary_knowledge_source: STRING}
- biolink:expressed_in {predicate: STRING, publications: LIST}
- biolink:gene_associated_with_condition {predicate: STRING, primary_knowledge_source: STRING, provided_by: STRING}
- biolink:genetically_associated_with {predicate: STRING, primary_knowledge_source: STRING}
- biolink:has_disease {predicate: STRING, publications: LIST}
- biolink:has_gene {predicate: STRING, publications: LIST}
- biolink:has_participant {predicate: STRING, primary_knowledge_source: STRING}
- biolink:has_phenotype {publications: LIST, primary_knowledge_source, disease_context_qualifier: STRING}
- biolink:has_sequence_variant {predicate: STRING}
- biolink:has_mode_of_inheritance {predicate: STRING, publications: List}
- biolink:homologous_to {predicate: STRING}
- biolink:interacts_with {predicate: STRING, publications: LIST}
- biolink:is_sequence_variant_of {predicate: STRING, primary_knowledge_source: STRING}
- biolink:model_of {predicate: STRING, publications: LIST, has_evidence: LIST}
- biolink:orthologous_to {predicate: STRING, primary_knowledge_source: STRING}
- biolink:same_as {predicate: STRING, primary_knowledge_source: STRING}
- biolink:subclass_of {predicate: STRING, primary_knowledge_source: STRING}

The relationships:
(:biolink:Gene)-[:biolink:causes]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:gene_associated_with_condition]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:contributes_to]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:genetically_associated_with]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:associated_with_increased_likelihood_of]->(:biolink:Disease)
(:biolink:Gene)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:Gene)-[:biolink:orthologous_to]->(:biolink:Gene)
(:biolink:Gene)-[:biolink:interacts_with]->(:biolink:Gene)
(:biolink:SequenceVariant)-[:biolink:is_sequence_variant_of]->(:biolink:Gene)
(:biolink:SequenceVariant)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:Disease)-[:biolink:has_phenotype]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:subclass_of]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:same_as]->(:biolink:PhenotypicFeature)
(:biolink:PhenotypicFeature)-[:biolink:homologous_to]->(:biolink:PhenotypicFeature)
(:biolink:Genotype)-[:biolink:model_of]->(:biolink:Disease)
(:biolink:Genotype)-[:biolink:has_sequence_variant]->(:biolink:SequenceVariant)
"""