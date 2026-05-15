import pandas as pd
import streamlit as st
import time

from neo4j_viz import Node, Relationship, VisualizationGraph
import streamlit.components.v1 as components

from src.rag import DiMonarchKG

# ══════════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

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
        st.title("Configuración")
        st.markdown("Ajustes del motor de razonamiento")

        llm_model = st.selectbox("Generative model", ["GPT-5.4"])
        temperature  = st.slider("Temperature (Creativity vs. Precision)", 0.0, 1.0, 0.0, 0.1)
        graph_height = st.slider("Graph height (px)", 300, 900, 520, 50)
        st.divider()
        st.caption("Proyecto TFM - Clinical GraphRAG")

    # Main area --------------
    st.title("🧬 Clinical GraphRAG")
    st.markdown("""
    Sistema de priorización de genes e interpretación de variantes basado en grafos de conocimiento. 
    Introduce los datos fenotípicos (términos HPO) y/o clínicos del paciente para obtener un informe.
    """)

    # --- ENTRADA DE DATOS ---
    col1, col2 = st.columns([2, 1])

    with col1:
        caso_clinico = st.text_area(
            "Descripción Clínica / Fenotipo (Términos HPO)",
            height=150,
            placeholder="Ej: Paciente con retraso global del desarrollo (HP:0001263), convulsiones atónicas (HP:0010819) y puente nasal ancho (HP:0000431)..."
        )

    with col2:
        genes_candidatos = st.text_input("Genes candidatos / VUS (Opcional)", placeholder="Ej: SLC6A1, SCN8A...")
        tipo_analisis = st.radio("Tipo de consulta", ["Priorización de genes", "Explicación de variante"])

    # --- BOTÓN DE EJECUCIÓN ---
    if st.button("🧠 Ejecutar Razonamiento GraphRAG", type="primary", use_container_width=True):

        if not caso_clinico:
            st.warning("⚠️ Por favor, introduce la descripción clínica del paciente.")
        else:
            # Spinner de carga mientras el modelo piensa
            with st.spinner('Consultando DIMonarchKG y generando inferencias...'):

                query = f"""
                Case report:
                {caso_clinico}
                
                Candidate genes:
                {genes_candidatos}
                """

                res = rag.search(query, return_context=True)

                context_items = []
                for item in res.response.retriever_result.items:
                    context_items.append(item.metadata['raw'])
                context_df = pd.DataFrame(context_items)

            # --- MOSTRAR RESULTADOS EN PESTAÑAS ---
            st.success("Análisis completado.")

            tab_entities, tab_informe, tab_evidencia, tab_grafo = st.tabs([
                "🔍 Entities Identified",
                "📝 Informe Diagnóstico",
                "🔍 Evidencia (Caja de Cristal)",
                "🕸️ Visualización del Grafo"
            ])

            with tab_entities:
                st.markdown("### Entities linked")
                st.markdown(res.query)
                #linked_data = []
                #for item in res.linked:
                #    linked_data.append(item.selected)
                #st.dataframe(pd.DataFrame(linked_data))


            with tab_informe:
                st.markdown(res.response.answer)

            with tab_evidencia:
                st.markdown("### Tripletas (Sujeto - Predicado - Objeto):")
                st.dataframe(context_df)

            # with tab_grafo:
            #     st.markdown(
            #         "*(Opcional)* Aquí puedes integrar librerías como `streamlit-agraph` o `pyvis` para renderizar visualmente los nodos interactivos.")
        # ── TAB: Grafo (neo4j-viz) ────────────────────────────────────────────────
            with tab_grafo:
                st.markdown('<p class="section-header">Subgraph — neo4j-viz</p>',
                            unsafe_allow_html=True)

                # ── Construir y renderizar el grafo ───────────────────────────
                vg = retriever_to_neo4j_viz(res.response.retriever_result)
                html_obj = vg.render()  # IPython.display.HTML
                components.html(html_obj.data, height=graph_height, scrolling=False)

                # ── Leyenda de categorías ─────────────────────────────────────
                st.markdown("**Categorías**")
                render_legend(res.response.retriever_result)

                # ── Tabla de relaciones del subgrafo ──────────────────────────
                #st.markdown("**Relaciones**")
                #rel_df = df[["subject", "relationship", "object", "source_kb"]]
                #st.dataframe(rel_df, use_container_width=True, height=200)
