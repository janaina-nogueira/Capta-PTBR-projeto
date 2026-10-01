# CAPTA-PTBR

**Corpus e recursos computacionais para investigação do capacitismo linguístico em Português Brasileiro**

O **CAPTA-PTBR** é um projeto de pesquisa voltado à identificação e análise computacional de manifestações de **capacitismo linguístico em Português Brasileiro (PT-BR)**.

O projeto reúne recursos desenvolvidos ao longo da pesquisa, incluindo corpus anotado, modelos de linguagem ajustados para classificação, resultados experimentais, códigos de análise e artefatos utilizados na avaliação dos modelos.

O objetivo é contribuir para o desenvolvimento de métodos de Processamento de Linguagem Natural (PLN) mais sensíveis ao contexto, capazes de distinguir manifestações capacitistas de usos legítimos da linguagem relacionados à deficiência.

---

## Sobre o projeto

A identificação automática do capacitismo apresenta desafios que vão além da presença de determinadas palavras.

Termos relacionados à deficiência podem ocorrer em diferentes contextos, incluindo usos clínicos, descritivos, informativos e sociais, sem necessariamente constituírem manifestações discriminatórias.

Por outro lado, determinadas construções linguísticas podem empregar referências à deficiência como forma de insulto, desqualificação, metáfora depreciativa ou atribuição negativa de capacidade.

Nesse contexto, o CAPTA-PTBR investiga como informações linguísticas e contextuais podem contribuir para a identificação computacional dessas manifestações em textos escritos em Português Brasileiro.

---

## Construção do CAPTA-PTBR

A construção do recurso foi organizada em diferentes etapas.

### Estágio 1 — Recuperação por padrões linguísticos

O primeiro estágio foi desenvolvido a partir da aplicação de **padrões léxico-sintáticos** sobre o corpus TuPy-E.

Foram recuperadas:

- **781 ocorrências agregadas**;
- **741 sentenças distintas**;
- **633 sentenças elegíveis** após a análise dos candidatos.

A seleção considerou sentenças que apresentavam caracterização ou citação de pessoa ou grupo, permitindo concentrar a análise em contextos potencialmente relevantes para a manifestação do capacitismo linguístico.

### Estágio 2 — Anotação manual

A etapa seguinte envolveu a construção de uma amostra com **1.500 sentenças** submetidas à anotação manual.

O conjunto resultante contém:

- **588 sentenças capacitistas**;
- **912 sentenças não capacitistas**.

Além da identificação binária da presença de capacitismo, as manifestações positivas foram caracterizadas considerando aspectos como categoria e polaridade.

Esse processo permite investigar o fenômeno considerando não apenas ocorrências lexicais isoladas, mas também o contexto em que os termos são empregados.

---

## Modelagem computacional

Os experimentos utilizam modelos baseados no **BERTimbau Base**, permitindo investigar o impacto da incorporação dos exemplos anotados do CAPTA-PTBR no reconhecimento da classe capacitista.

O projeto contempla experimentos em diferentes configurações, incluindo:

- treinamento utilizando dados do TuPy-E;
- enriquecimento dos dados com o CAPTA-PTBR;
- avaliação em dados externos;
- aplicação sobre o BiasTube-PTBR;
- comparação de modelos com e sem adaptação ao domínio;
- **Domain-Adaptive Pretraining (DAPT)**.

A adaptação de domínio utiliza treinamento adicional por **Masked Language Modeling (MLM)** sobre textos do domínio analisado.

---

## Validação das predições

Além da avaliação quantitativa dos modelos, o projeto inclui uma etapa de **validação das predições**.

As classificações produzidas automaticamente são confrontadas com anotações humanas, permitindo analisar casos de:

- verdadeiros positivos;
- verdadeiros negativos;
- falsos positivos;
- falsos negativos.

Essa etapa contribui para compreender não apenas o desempenho agregado dos modelos, mas também os tipos de construções linguísticas que apresentam maior dificuldade para a classificação automática.

---

## Métricas de avaliação

Os modelos são avaliados utilizando métricas adequadas à classificação binária e ao desbalanceamento entre classes.

Entre as principais métricas utilizadas estão:

| Métrica | Descrição |
|---|---|
| **Precision+** | Precisão para a classe capacitista |
| **Recall+** | Recuperação da classe capacitista |
| **F1+** | F1-score da classe capacitista |
| **F1 Macro** | Média do F1 entre as classes |
| **AUROC** | Área sob a curva ROC |
| **AUPRC+** | Área sob a curva Precision-Recall da classe positiva |

A análise prioriza métricas específicas da classe positiva para evitar que o desempenho sobre a classe majoritária oculte dificuldades na identificação das manifestações capacitistas.

---

## Recursos disponibilizados

Este repositório reúne os principais artefatos computacionais produzidos durante a pesquisa:

```text
CAPTA-PTBR/
│
├── corpus/
│   ├── estagio_1/
│   ├── estagio_2/
│   └── predicao/
│
├── models/
│   ├── bertimbau_capta/
│   ├── bertimbau_sem_dapt/
│   └── berttube_dapt/
│
├── analises/
│
├── resultados/
│
├── pages/
│
├── assets/
│
├── Home.py
├── site_utils.py
├── requirements.txt
├── CITATION.cff
└── README.md
```

### `corpus/`

Contém os conjuntos de dados produzidos e utilizados nas diferentes etapas da pesquisa.

### `models/`

Contém os modelos e artefatos derivados dos experimentos de treinamento e adaptação de domínio.

Arquivos de grande porte são versionados utilizando **Git LFS**.

### `analises/`

Contém scripts utilizados no processamento, treinamento, predição e análise dos experimentos.

### `resultados/`

Reúne resultados derivados das análises e avaliações realizadas durante a pesquisa.

### `pages/`

Contém as páginas da interface web desenvolvida em Streamlit para apresentação e disponibilização dos recursos do projeto.

---

## Website

O projeto também possui uma interface desenvolvida em **Streamlit** para facilitar a exploração dos recursos produzidos.

O website está organizado nas seguintes seções:

- **Home** — apresentação geral do projeto;
- **Corpus** — descrição, visualização e acesso aos conjuntos de dados;
- **Modelos** — modelos desenvolvidos durante os experimentos;
- **Análises** — códigos e artefatos das análises;
- **Resultados** — síntese dos principais resultados experimentais;
- **Sobre** — informações acadêmicas e institucionais.

---

## Executando localmente

Clone o repositório:

```bash
git clone <URL-DO-REPOSITORIO>
```

Entre na pasta:

```bash
cd Capta-PTBR-projeto
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o website:

```bash
streamlit run Home.py
```

O Streamlit disponibilizará a aplicação localmente no navegador.

---

## Tecnologias

O projeto utiliza principalmente:

- Python;
- Streamlit;
- Pandas;
- Scikit-learn;
- PyTorch;
- Transformers;
- BERTimbau;
- Git;
- Git LFS.

---

## Contexto acadêmico

O CAPTA-PTBR foi desenvolvido no contexto de pesquisa de pós-graduação da **Universidade Federal de Mato Grosso do Sul (UFMS)**, na **Faculdade de Computação (FACOM)**.

A pesquisa integra conhecimentos de **Processamento de Linguagem Natural, Aprendizado de Máquina, Linguística e Estudos da Deficiência**, buscando compreender o capacitismo como um fenômeno que depende não apenas do léxico, mas também do contexto linguístico e social em que uma expressão é utilizada.

---

## Autoria

**Janaína Nogueira de Souza Lopes**

Universidade Federal de Mato Grosso do Sul — UFMS  
Faculdade de Computação — FACOM

### Orientação

- Prof. Dr. Anderson Corrêa de Lima
- Profa. Dra. Valéria Quadros dos Reis
- Prof. Dr. Amaury Antônio de Castro Junior

---

## Citação

Caso utilize o CAPTA-PTBR, os modelos ou demais recursos disponibilizados neste repositório em trabalhos acadêmicos, consulte o arquivo:

```text
CITATION.cff
```

para obter as informações atualizadas de citação do projeto.

---

## Uso responsável

O corpus contém exemplos linguísticos utilizados para estudar manifestações de capacitismo e, portanto, pode incluir **linguagem ofensiva, discriminatória ou potencialmente sensível**.

Esses conteúdos são disponibilizados exclusivamente para fins de pesquisa, análise científica e desenvolvimento de métodos computacionais para identificação e mitigação de comportamentos discriminatórios.

A presença de determinado termo no corpus **não implica que o termo seja inerentemente capacitista**. A interpretação depende do contexto linguístico e discursivo em que ocorre.

---

## Status

**CAPTA-PTBR — versão 1.0**

O projeto encontra-se em desenvolvimento no contexto da pesquisa de mestrado. Recursos, documentação e resultados podem ser atualizados conforme a consolidação dos experimentos e da dissertação.
