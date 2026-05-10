import json
import logging
import os
import random

import numpy as np
import pandas as pd

from dotenv import load_dotenv
from neo4j.exceptions import ClientError

from src.core.entity_linking import EntityLinking
from src.embedders import embedder
from src.graph.neo4j_client import driver, index_map
from src.llms import ner_llm
from src.retrievers.entity_linker_retriever import EntityLinkingRetriever
from src.retrievers.phenotypic_similarity_retriever import PhenotypeExtraction

def generate_synonyms_dataset(session, label, namespace, n: int = 100):
    result = session.run(f"""
    MATCH (d:`{label}` {{namespace: $namespace}})
    WHERE size(d.synonym) > 0
    WITH d.id as id, d.name as name, apoc.coll.randomItems(d.synonym, 1)[0] as synonym, rand() as r
    ORDER BY r 
    WHERE name <> synonym
    RETURN id, name, synonym
    LIMIT $n
    """, n=n, namespace=namespace)
    synonym_dataset = pd.DataFrame(list(map(dict, result)))
    return synonym_dataset


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 1. Quitar el límite de ancho de la "tabla" completa
    pd.set_option('display.width', None)

    # 2. Impedir que las columnas se muevan "abajo" si no caben
    pd.set_option('display.expand_frame_repr', False)

    # 3. Quitar el límite de caracteres dentro de cada celda
    pd.set_option('display.max_colwidth', None)

    # 4. Asegurar que se vean todas las columnas
    pd.set_option('display.max_columns', None)

    # 5. Asegurar que se vean todas las filas
    pd.set_option('display.max_rows', None)

    session = driver.session(database=os.environ['NEO4J_DATABASE'])

    df_hp_synonym = generate_synonyms_dataset(session, label="biolink:PhenotypicFeature", namespace='HP', n=100)
    df_disease_synonym = generate_synonyms_dataset(session, label="biolink:Disease", namespace='MONDO', n=100)

    linker = EntityLinking(driver=driver, embedder=embedder)

    hp_solved = []
    for idx, item in df_hp_synonym.iterrows():
        item_dict = dict(item)
        linked = linker.vector_search_link(query=item_dict['synonym             '], label="biolink:PhenotypicFeature", index="phenotypic_feature_index", namespace="HP", k=50)
        item_dict['solved'] = linked[0].id
        ids = list(map(lambda i: i.id, linked))
        try:
            idx = ids.index(item_dict['id'])
            item_dict['MRR'] = 1/(idx + 1)
            item_dict['K'] = idx + 1
        except ValueError:
            item_dict['MRR'] = 0.00
            item_dict['K'] = 51
        hp_solved.append(item_dict)

    ds_solved = []
    for idx, item in df_disease_synonym.iterrows():
        item_dict = dict(item)
        linked = linker.vector_search_link(query=item_dict['synonym'], label='biolink:Disease', index='disease_index', namespace='MONDO',
                                           k=50)
        item_dict['solved'] = linked[0].id
        ids = list(map(lambda i: i.id, linked))
        try:
            idx = ids.index(item_dict['id'])
            item_dict['MRR'] = 1 / (idx + 1)
            item_dict['K'] = idx + 1
        except ValueError:
            item_dict['MRR'] = 0.00
            item_dict['K'] = 51
        ds_solved.append(item_dict)


    df_hp_synonym = pd.DataFrame(hp_solved)
    df_ds_synonym = pd.DataFrame(ds_solved)


    metrics = {'phenotype': {}, 'disease': {}}
    metrics['phenotype']['MRR'] = df_hp_synonym['MRR'].mean()
    metrics['phenotype']['Recall@1'] = np.mean(df_hp_synonym['K'] <= 1)
    metrics['phenotype']['Recall@3'] = np.mean(df_hp_synonym['K'] <= 3)
    metrics['phenotype']['Recall@5'] = np.mean(df_hp_synonym['K'] <= 5)

    metrics['disease']['MRR'] = df_ds_synonym['MRR'].mean()
    metrics['disease']['Recall@1'] = np.mean(df_ds_synonym['K'] <= 1)
    metrics['disease']['Recall@3'] = np.mean(df_ds_synonym['K'] <= 3)
    metrics['disease']['Recall@5'] = np.mean(df_ds_synonym['K'] <= 5)

    print(json.dumps(metrics, indent=4))
    df_hp_synonym.to_csv(f"/tmp/phenotype_synonyms_dataset.csv", header=True, index=False)
    df_ds_synonym.to_csv(f"/tmp/disease_synonyms_dataset.csv", header=True, index=False)

    exit(0)

    #
    #
    # elr = EntityLinkingRetriever(driver=driver, embedder=embedder, llm=ner_llm, entities_model=PhenotypeExtraction, index_map=index_map)
    #
    #
    # result = session.run("""
    # MATCH (n:`biolink:PhenotypicFeature`)
    # WHERE n.namespace = 'HP'
    # WITH collect(n) AS all_phenotypes
    # RETURN apoc.coll.randomItems(all_phenotypes, $top_n) as samples
    # """,
    # top_n=100)
    # sampling = result.single()
    # out_df = []
    # for item in sampling['samples']:
    #
    #     if not 'synonym' in item:
    #         logging.info("skip")
    #         continue
    #
    #     #qtext = random.sample(item.get("description"), k=1)[0]
    #     qtext = item.get("synonym")[0]
    #
    #     vc_hits = elr.linker.vector_search(session=session, mention=qtext, v_index="phenotypic_feature_index", namespace='HP', threshold=0.7, top_k=50)
    #     try:
    #         ft_hits = elr.linker.fulltext_search(session=session, mention=qtext, ft_index="phenotypic_feature_fulltext_index", threshold=1.0)
    #     except ClientError as err:
    #         ft_hits = []
    #
    #     if len(ft_hits) > 0:
    #         vc_df = pd.DataFrame(vc_hits)
    #         vc_df['score'] = vc_df['score'] / vc_df['score'].max()
    #         ft_df = pd.DataFrame(ft_hits)
    #         ft_df['score'] = ft_df['score'] / ft_df['score'].max()
    #         hits_scores = vc_df.merge(ft_df, how='left', on='id', suffixes=('', '_ft'))
    #         hits_scores['combined_score'] = 0.60 * hits_scores['score'] + 0.40 * hits_scores['score_ft']
    #         hits_scores.sort_values('combined_score', ascending=False, inplace=True)
    #
    #         hits = hits_scores.loc[:, ['id', 'name', 'combined_score']].rename(columns={'combined_score': 'score'}).to_dict(
    #             orient="records")
    #     else:
    #         hits = vc_hits
    #         logging.warning("ONLY VECTOR INDEX SEARCH CONSIDERED")
    #
    #     #hits = resolve_entities(emb=embedder, query_text=qtext, session=session, threshold=0.8, k=100)
    #     ids = np.array(list(map(lambda h: h['id'], hits)))
    #     idx = np.argwhere(ids == item.get("id"))
    #     try:
    #         idx = idx[0][0]
    #         hit = hits[idx]
    #         out_df.append(dict(
    #             idx=idx,
    #             text=qtext,
    #             test_id=item.get('id'),
    #             hit_name=hit.get("name"),
    #             best_id=hits[0].get('id'),
    #             best_name=hits[0].get('name'),
    #             MRR=1/(idx+1)
    #         ))
    #     except IndexError:
    #         idx = None
    #         out_df.append(dict(
    #             idx=idx,
    #             text=qtext,
    #             test_id=item.get('id'),
    #             hit_name=None,
    #             best_id=None,
    #             best_name=None,
    #             MRR=None
    #         ))
    # out_df = pd.DataFrame(out_df)
    # print(out_df.loc[out_df.idx != 0])
    # for k in range(1, 6):
    #     print(f"Recall@{k}: {np.mean(out_df['idx']+1 <= k)}")
    # print(f"Average MRR: {np.mean(out_df['MRR'])}")
    # print(f"N={out_df.shape[0]}")