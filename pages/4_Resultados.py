import streamlit as st
import pandas as pd

from site_utils import apply_theme, header_logos, footer


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Resultados | Capta-PTBR",
    page_icon="📊",
    layout="wide"
)

apply_theme()
header_logos()


# ============================================================
# CABEÇALHO
# ============================================================

st.title("Resultados")

st.markdown(
    """
    Esta seção apresenta uma síntese dos principais resultados obtidos
    durante a construção, validação e avaliação experimental do
    **CAPTA-PTBR**.
    """
)


# ============================================================
# 1. CONSTRUÇÃO DO CAPTA-PTBR
# ============================================================

st.header("1. Construção do CAPTA-PTBR")

st.markdown(
    """
    A construção do corpus foi realizada em duas etapas complementares.
    No **Estágio 1**, padrões léxico-sintáticos foram utilizados para
    recuperar sentenças potencialmente relacionadas ao fenômeno investigado.
    No **Estágio 2**, foi constituída uma amostra ampliada para anotação
    manual, incorporando exemplos positivos e negativos.
    """
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Ocorrências recuperadas",
    "781"
)

c2.metric(
    "Sentenças distintas",
    "741"
)

c3.metric(
    "Elegíveis",
    "633"
)

c4.metric(
    "Corpus anotado",
    "1.500"
)

st.info(
    """
    O Estágio 1 permitiu identificar e validar candidatos a partir dos
    padrões linguísticos, enquanto o Estágio 2 ampliou o conjunto para
    possibilitar a anotação de exemplos capacitistas e não capacitistas.
    """
)


# ============================================================
# 2. ANOTAÇÃO MANUAL
# ============================================================

st.header("2. Anotação manual")

st.markdown(
    """
    O conjunto do Estágio 2 contém **1.500 sentenças anotadas
    manualmente** quanto à presença de conteúdo capacitista.
    """
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Sentenças anotadas",
    "1.500"
)

c2.metric(
    "Capacitistas",
    "588"
)

c3.metric(
    "Não capacitistas",
    "912"
)


st.subheader("Distribuição das categorias")

categorias = pd.DataFrame({
    "Categoria": [
        "Insulto direto",
        "Uso metafórico",
        "Uso aparentemente neutro"
    ],
    "Sentenças": [
        565,
        18,
        5
    ]
})

st.dataframe(
    categorias,
    use_container_width=True,
    hide_index=True
)

st.markdown(
    """
    Entre as **588 sentenças classificadas como capacitistas**, houve
    predominância de **insultos diretos (565)**. Os usos metafóricos
    corresponderam a **18 casos**, enquanto **5 sentenças** foram
    classificadas como uso aparentemente neutro.
    """
)


st.subheader("Polaridade")

polaridade = pd.DataFrame({
    "Polaridade": [
        "Negativa",
        "Positiva",
        "Neutra"
    ],
    "Sentenças": [
        578,
        6,
        4
    ]
})

st.dataframe(
    polaridade,
    use_container_width=True,
    hide_index=True
)

st.markdown(
    """
    A polaridade das manifestações capacitistas foi predominantemente
    **negativa**, observada em **578 das 588 sentenças**, seguida por
    6 ocorrências positivas e 4 neutras.
    """
)


# ============================================================
# 3. IMPACTO DO CAPTA-PTBR
# ============================================================

st.header("3. Impacto do CAPTA-PTBR no treinamento")

st.markdown(
    """
    Para avaliar a contribuição do corpus, foram comparados dois
    experimentos com o **BERTimbau Base**: o primeiro utilizando apenas
    o TuPy-E e o segundo incorporando ao treinamento as sentenças
    anotadas do CAPTA-PTBR.
    """
)

resultados_capta = pd.DataFrame({

    "Experimento": [
        "Fase 1 · TuPy-E",
        "Fase 2 · TuPy-E + CAPTA-PTBR"
    ],

    "Precision+": [
        0.3333,
        0.7609
    ],

    "Recall+": [
        0.0500,
        0.8898
    ],

    "F1+": [
        0.0870,
        0.8203
    ],

    "F1macro": [
        0.5429,
        0.9088
    ],

    "AUROC": [
        0.8725,
        0.9697
    ],

    "AUPRC+": [
        0.0772,
        0.8645
    ]
})

st.dataframe(
    resultados_capta,
    use_container_width=True,
    hide_index=True
)


# Destaques

c1, c2, c3 = st.columns(3)

c1.metric(
    "Recall+",
    "0,8898",
    "Fase 2"
)

c2.metric(
    "F1+",
    "0,8203",
    "Fase 2"
)

c3.metric(
    "AUPRC+",
    "0,8645",
    "Fase 2"
)


st.success(
    """
    A incorporação do CAPTA-PTBR produziu aumento expressivo na
    capacidade do modelo de reconhecer a classe capacitista.
    O Recall+ passou de **0,0500 para 0,8898**, o F1+ de
    **0,0870 para 0,8203** e a AUPRC+ de **0,0772 para 0,8645**.
    """
)

st.markdown(
    """
    Esses resultados indicam que o enriquecimento dos dados com
    exemplos anotados e contextualizados do CAPTA-PTBR reduziu a
    dificuldade inicial do modelo em aprender a classe minoritária,
    produzindo maior equilíbrio entre as classes.
    """
)


# ============================================================
# 4. TRANSFERÊNCIA PARA BIASTUBE
# ============================================================

st.header("4. Transferência para o BiasTube-PTBR")

st.markdown(
    """
    Após o enriquecimento com o CAPTA-PTBR, os experimentos avançaram
    para o **BiasTube-PTBR**, composto por mais de 500 mil comentários
    do YouTube. Essa etapa permitiu investigar a transferência do
    conhecimento aprendido para dados provenientes de um domínio
    digital distinto.
    """
)


st.subheader("BERTimbau sem DAPT")

st.markdown(
    """
    Na configuração **sem adaptação de domínio**, o BERTimbau apresentou
    bom equilíbrio entre precisão e recuperação da classe positiva no
    conjunto de validação.
    """
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Precision+",
    "0,7787"
)

c2.metric(
    "Recall+",
    "0,8051"
)

c3.metric(
    "F1+",
    "0,7917"
)


# ============================================================
# 5. DAPT
# ============================================================

st.header("5. Adaptação de domínio — DAPT")

st.markdown(
    """
    Também foi avaliada uma estratégia de **Domain-Adaptive
    Pretraining (DAPT)**. Nessa configuração, o BERTimbau Base
    passou por treinamento adicional com objetivo de linguagem
    mascarada sobre textos do BiasTube-PTBR, originando o
    **BERTtube**.
    """
)


resultados_dapt = pd.DataFrame({

    "Modelo": [
        "BERTtube · com DAPT"
    ],

    "Accuracy": [
        0.9927
    ],

    "Precision+": [
        0.6687
    ],

    "Recall+": [
        0.9068
    ],

    "F1+": [
        0.7698
    ],

    "F1macro": [
        0.8830
    ],

    "AUROC": [
        0.9816
    ],

    "AUPRC+": [
        0.8038
    ]
})

st.dataframe(
    resultados_dapt,
    use_container_width=True,
    hide_index=True
)


c1, c2, c3 = st.columns(3)

c1.metric(
    "Precision+",
    "0,6687"
)

c2.metric(
    "Recall+",
    "0,9068"
)

c3.metric(
    "F1+",
    "0,7698"
)


st.info(
    """
    O DAPT não produziu ganhos globais expressivos e consistentes.
    As principais métricas permaneceram em patamares semelhantes,
    mas houve mudança no comportamento do modelo.
    """
)

st.markdown(
    """
    O **BERTtube com DAPT apresentou maior Recall+**, indicando maior
    sensibilidade para recuperar ocorrências capacitistas. Em contrapartida,
    o **BERTimbau sem DAPT apresentou maior Precision+**, mantendo um
    comportamento mais conservador.

    Assim, a adaptação de domínio alterou principalmente o equilíbrio
    entre **falsos negativos e falsos positivos**, em vez de produzir
    uma melhoria global inequívoca no desempenho.
    """
)


# ============================================================
# 6. SÍNTESE
# ============================================================

st.header("6. Síntese dos resultados")

st.markdown(
    """
    Os experimentos evidenciam três resultados principais:

    **1. Construção do recurso linguístico.**  
    O processo de recuperação, seleção e anotação resultou em um corpus
    contextualizado em Português Brasileiro, com **1.500 sentenças
    anotadas manualmente**.

    **2. Contribuição do CAPTA-PTBR.**  
    A incorporação das sentenças anotadas produziu melhora substancial
    na identificação da classe capacitista, especialmente em
    **Recall+, F1+ e AUPRC+**.

    **3. Adaptação ao domínio.**  
    O DAPT sobre o BiasTube-PTBR modificou o comportamento do modelo,
    aumentando sua sensibilidade à classe positiva, mas sem apresentar
    ganhos globais consistentes em relação à configuração sem DAPT.
    """
)


footer()