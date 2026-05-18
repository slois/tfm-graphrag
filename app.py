import random

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from neo4j_viz import Node, Relationship, VisualizationGraph
from src.rag import DiMonarchKG
from test.test_case_report import cases

CATEGORY_COLORS = {
    "biolink:Gene": "#6c8cff",
    "biolink:Pathway": "#ff6c8c",
    "biolink:Disease": "#8cffa0",
    "biolink:Drug": "#ffd96c",
    "biolink:Protein": "#c46cff",
    "biolink:ChemicalEntity": "#6cffed",
    "biolink:PhenotypicFeature": "#ff9f6c",
}
DEFAULT_COLOR = "#888ea8"

TAB_CONFIGS = {
    "report": "📝 Report",
    "entities": "🖇️ Entities Identified",
    "evidence": "🔎 Evidence Paths"
}


def render_tab(key: str, df: pd.DataFrame):
    if key == "report":
        st.markdown(res.response.answer)

    elif key == "evidence":
        st.subheader("Triplets (Subject - Predicate - Object")
        #st.markdown("### Tripletas (Sujeto - Predicado - Objeto):")
        st.dataframe(df, use_container_width=True)

    elif key == "entities":
        st.subheader("Entities Linked")
        st.dataframe(df, use_container_width=True)



def retriever_to_neo4j_viz(retriever_result):
    """
    Convierte los items del retriever en un VisualizationGraph.
    Cada item representa un triple: Subject -[Relationship]-> Object
    """
    nodes_dict = {}   # id → Node  (para deduplicar)
    relationships = []

    # Paleta por categoría biolink
    category_colors = {
        "biolink:Gene": "#6c8cff",
        "biolink:Pathway": "#ff6c8c",
        "biolink:Disease": "#8cffa0",
        "biolink:PhenotypicFeature": "#ffd96c",
        "biolink:BiologicalProcess":  "#c46cff",
    }

    for item in retriever_result.items:
        d = item.metadata['raw']

        subj_id  = d.get("Subject_id", "")
        subj_name = d.get("Subject_name", subj_id)
        subj_cat  = d.get("Subject_category", "")

        obj_id   = d.get("Object_id", "")
        obj_name  = d.get("Object_name", obj_id)
        obj_cat   = d.get("Object_category", "")

        rel_type  = d.get("Relationship_type", "").replace("biolink:", "")
        source    = d.get("Relationship_primary_knowledge_source", "")

        # Añadir nodos (deduplicando por id)
        if subj_id and subj_id not in nodes_dict:
            nodes_dict[subj_id] = Node(
                id=subj_id,
                caption=subj_name,
                size=20,
                color=category_colors.get(subj_cat, "#aaaaaa"),
            )

        if obj_id and obj_id not in nodes_dict:
            nodes_dict[obj_id] = Node(
                id=obj_id,
                caption=obj_name,
                size=16,
                color=category_colors.get(obj_cat, "#aaaaaa"),
            )

        # Añadir relación
        if subj_id and obj_id:
            relationships.append(Relationship(
                source=subj_id,
                target=obj_id,
                caption=rel_type,
            ))

    vg = VisualizationGraph(
        nodes=list(nodes_dict.values()),
        relationships=relationships,
    )
    return vg


def render_legend(retriever_result) -> None:
    """Pildoras de color por categoría biolink presentes en el resultado."""
    cats = set()
    for item in retriever_result.items:
        d = item.metadata['raw']
        cats.add(d.get("Subject_category", ""))
        cats.add(d.get("Object_category", ""))
    cats.discard("")

    pills = " ".join(
        f'<span style="background:{CATEGORY_COLORS.get(c, DEFAULT_COLOR)};color:#0d0f14;'
        f'padding:3px 12px;border-radius:12px;font-size:.75rem;font-weight:700;margin:2px">'
        f'{c.replace("biolink:", "")}</span>'
        for c in sorted(cats)
    )
    st.markdown(pills, unsafe_allow_html=True)


if __name__ == '__main__':
    # GraphRAG ---------------
    rag = DiMonarchKG()

    # Page configuration -----
    st.set_page_config(
        page_title="Clinical GraphRAG",
        page_icon="🧬",
        layout="wide"
    )

    # Side bar ---------------
    with st.sidebar:
        st.logo("img/uoc.png")
        st.title("Clinical GraphRAG")
        st.markdown("Ajustes del motor de razonamiento")
        llm_model = st.selectbox("Generative model", ["GPT-5.4"])
        temperature  = st.slider("Temperature (Creativity vs. Precision)", 0.0, 1.0, 0.0, 0.1)
        graph_height = st.slider("Graph height (px)", 300, 900, 520, 50)
        st.divider()
        st.caption("""
        This work presents the design, implementation and evaluation of *Clinical GraphRAG*, a *Graph Retrieval-Augmented Generation* architecture for diagnostic decision support in neurodevelopmental disorders. 
        The system operates on DIMonarchKG, a domain-specific biomedical knowledge graph derived from the public MonarchKG resource.
        """)
        st.divider()
        st.caption("Data Science Master's Disseration. Universitat Oberta de Catalunya")
        st.caption("Author: Sergio Lois, PhD")

    # Main area --------------
    st.title("🧬 Clinical GraphRAG")
    # --- ENTRADA DE DATOS ---
    main_col, graph_col = st.columns([1, 1])

    with main_col:
        caso_clinico = st.text_area(
            "Clinical description",
            height=200,
            placeholder="""A pediatric patient presented with moderate intellectual disability, global developmental delay, and microcephaly. The neonatal history was notable for a characteristic high-pitched, cat-like cry. Physical examination revealed facial dysmorphism including hypertelorism and micrognathia.

- Which disease are most likely to be related with these phenotypes and which genes are associated to them?
            """
        )
        launch_button = st.button("🧠 Launch GraphRAG", type="primary", use_container_width=True)

    if launch_button:
        if not caso_clinico:
            st.warning("⚠️ Por favor, introduce la descripción clínica del paciente.")
        else:
            # Spinner de carga mientras el modelo piensa
            with st.spinner('Consultando DIMonarchKG y generando inferencias...'):

                query = f"""
                Case report:
                {caso_clinico}
                """

                res = rag.search(query, return_context=True)

                if len(res.response.retriever_result.items) > 0:
                    context_items = []
                    for item in res.response.retriever_result.items:
                        context_items.append(item.metadata['raw'])

                    # Context dataframe
                    context_df = pd.DataFrame(context_items)
                else:
                    context_df = None

                # Entities dataframe
                if len(res.linked) > 0:
                    entities_linked_df = pd.DataFrame(
                        data=[dict(mention=item.mention, **item.selected.dict()) for item in res.linked if item.selected is not None])
                else:
                    entities_linked_df = None

                results = {
                    'report': res.response.answer,
                    'evidence': context_df,
                    'entities': entities_linked_df,
                }

            # --- MOSTRAR RESULTADOS EN PESTAÑAS ---
            with main_col:
                st.success("Análisis completado.")

            available_tabs = [tab for tab, res in results.items() if res is not None]

            tab_objects = st.tabs([TAB_CONFIGS[tab_key] for tab_key in available_tabs])

            for tab, label in zip(tab_objects, available_tabs):
                with tab:
                    render_tab(label, results[label])

            with graph_col: #tab_grafo:
                st.markdown('<p class="section-header">Subgraph</p>', unsafe_allow_html=True)

                vg = retriever_to_neo4j_viz(res.response.retriever_result)
                html_obj = vg.render()  # IPython.display.HTML
                components.html(html_obj.data, height=graph_height, scrolling=False)

                st.markdown("**Categorías**")
                render_legend(res.response.retriever_result)
