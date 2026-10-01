import streamlit as st
from site_utils import apply_theme, header_logos, footer

st.set_page_config(page_title="Capta-PTBR", page_icon="◉", layout="wide", initial_sidebar_state="expanded")
apply_theme()
header_logos()

st.markdown("""
<div class="hero">
<div class="eyebrow">UFMS · FACOM · Programa de Pós-Graduação em Computação Aplicada</div>
<div class="hero-title">Capta-PTBR</div>
<div class="hero-sub"><b>Corpus e Recursos Computacionais para Pesquisa sobre Capacitismo Linguístico em Português Brasileiro.</b><br>
Uma plataforma para organização, preservação e divulgação dos recursos produzidos na pesquisa de mestrado.</div>
</div>
""", unsafe_allow_html=True)

st.subheader("O corpus em duas etapas")
c1,c2 = st.columns(2)
with c1:
    st.markdown("""<div class="card corpus-card">
    <div class="card-kicker">CAPTA-PTBR · ESTÁGIO 1</div>
    <div class="big">741 sentenças distintas</div>
    <p>Conjunto identificado a partir dos padrões léxico-sintáticos no TuPy-E. Os padrões produziram 781 ocorrências agregadas; em nível de sentença, correspondem a 741 sentenças distintas. Destas, 633 foram classificadas como caracterização/citação de pessoa.</p>
    <span class="pill">781 ocorrências</span><span class="pill">741 sentenças</span><span class="pill">633 elegíveis</span>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="card corpus-card">
    <div class="card-kicker">CAPTA-PTBR · ESTÁGIO 2</div>
    <div class="big">1.500 sentenças anotadas</div>
    <p>Conjunto de anotação manual composto pelas 633 sentenças elegíveis e por sentenças adicionais selecionadas aleatoriamente, permitindo incluir exemplos positivos e negativos.</p>
    <span class="pill">588 capacitistas</span><span class="pill">912 não capacitistas</span><span class="pill">13 anotadores</span>
    </div>""", unsafe_allow_html=True)

st.subheader("Recursos")

a, b, c, d = st.columns(4)

a.metric("Estágio 1", "741", "sentenças distintas")
b.metric("Estágio 2", "1.500", "sentenças anotadas")
c.metric("Capacitistas", "588", "validação manual")

d.metric(
    "Idioma",
    "PT-BR",
    "conteúdo no idioma",
)

st.markdown("### Explore")
x,y,z = st.columns(3)
with x:
    st.markdown('<div class="card corpus-card"><b>Corpus</b><p class="muted">Arquivos CSV, documentação dos dois estágios e protocolo de anotação.</p></div>', unsafe_allow_html=True)
with y:
    st.markdown('<div class="card corpus-card"><b>Modelos</b><p class="muted">Arquivos dos modelos, configurações, métricas e informações sobre treinamento e DAPT.</p></div>', unsafe_allow_html=True)
with z:
    st.markdown('<div class="card corpus-card"><b>Análises e Resultados</b><p class="muted">Código das análises, tabelas e síntese dos principais resultados da dissertação.</p></div>', unsafe_allow_html=True)

footer()
