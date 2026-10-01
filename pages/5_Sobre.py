import streamlit as st
from site_utils import apply_theme, header_logos, footer
st.set_page_config(page_title="Sobre | Capta-PTBR", page_icon="ℹ️", layout="wide")
apply_theme(); header_logos()
st.title("Sobre o projeto")
st.write("""
O **Capta-PTBR** é um recurso computacional desenvolvido no contexto da dissertação
**“Capacitismo Linguístico no Português Brasileiro: Uma Análise Computacional da Representação de Pessoas com Deficiência”**,
no Programa de Pós-Graduação em Computação Aplicada da Faculdade de Computação da Universidade Federal de Mato Grosso do Sul.

A pesquisa investiga manifestações de capacitismo linguístico em discursos digitais brasileiros por meio de técnicas de
Processamento de Linguagem Natural. O trabalho articula extração baseada em padrões léxico-sintáticos, validação manual e
modelagem supervisionada para construir recursos linguísticos e avaliar a identificação automática de manifestações capacitistas.
O BERTimbau Base é avaliado com e sem adaptação de domínio, permitindo investigar tanto o efeito do enriquecimento do conjunto
de treinamento quanto a transferência para comentários de redes sociais.
""")
st.subheader("Pesquisa")
st.markdown("""
**Autora:** Janaína Nogueira de Souza Lopes  
**Orientador:** Prof. Anderson Corrêa de Lima  
**Coorientadores:** Profa. Valéria Quadros dos Reis e Prof. Amaury Antônio de Castro Junior  
**Instituição:** Universidade Federal de Mato Grosso do Sul — UFMS  
**Unidade:** Faculdade de Computação — FACOM  
**Programa:** Pós-Graduação em Computação Aplicada — PPGCC
""")
st.link_button("GitHub · Janaína Nogueira", "https://github.com/janaina-nogueira")
st.subheader("Registro e versão")
st.write("Versão do portal: **CAPTA-PTBR v1.0**. Todos os direitos reservados.")
footer()
