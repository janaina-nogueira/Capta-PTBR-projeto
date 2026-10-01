from pathlib import Path

import pandas as pd
import streamlit as st

from site_utils import apply_theme, header_logos, footer


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Corpus | Capta-PTBR",
    page_icon="📚",
    layout="wide"
)

apply_theme()
header_logos()


# ============================================================
# CAMINHOS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

CORPUS_DIR = ROOT / "corpus"

ESTAGIO_1_DIR = CORPUS_DIR / "estagio_1"
ESTAGIO_2_DIR = CORPUS_DIR / "estagio_2"

VALIDACAO_DIR = CORPUS_DIR / "predicao"


# ============================================================
# FUNÇÕES
# ============================================================

def localizar_csv(pasta: Path):
    """
    Localiza o primeiro arquivo CSV existente na pasta.
    """

    if not pasta.exists():
        return None

    arquivos = sorted(
        pasta.glob("*.csv")
    )

    if not arquivos:
        return None

    return arquivos[0]


def carregar_csv(arquivo: Path):
    """
    Tenta carregar o CSV utilizando codificações comuns.
    """

    if arquivo is None:
        return None

    tentativas = [
        {"encoding": "utf-8"},
        {"encoding": "utf-8-sig"},
        {"encoding": "latin-1"}
    ]

    for configuracao in tentativas:

        try:
            return pd.read_csv(
                arquivo,
                **configuracao
            )

        except Exception:
            continue

    return None


def mostrar_download_csv(
    arquivo: Path,
    titulo: str,
    key: str
):
    """
    Exibe botão para download do CSV.
    """

    if arquivo is None:

        st.info(
            "Arquivo ainda não adicionado ao website."
        )

        return

    st.download_button(
        label=f"⬇ Baixar {titulo}",
        data=arquivo.read_bytes(),
        file_name=arquivo.name,
        mime="text/csv",
        key=key
    )


def visualizar_csv(
    arquivo: Path,
    limite: int = 50
):
    """
    Mostra uma amostra do CSV.
    """

    if arquivo is None:
        return

    df = carregar_csv(arquivo)

    if df is None:

        st.warning(
            "O arquivo existe, mas não foi possível "
            "visualizá-lo automaticamente."
        )

        return

    st.caption(
        f"{len(df):,} registros • "
        f"{len(df.columns)} colunas"
    )

    st.dataframe(
        df.head(limite),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.title("Corpus")

st.markdown(
    """
    O **Capta-PTBR** reúne os recursos linguísticos construídos
    durante a pesquisa sobre capacitismo linguístico em
    Português Brasileiro.

    O corpus foi desenvolvido em diferentes etapas, desde a
    recuperação de candidatos por padrões léxico-sintáticos até
    a anotação manual e a posterior validação das predições
    realizadas pelos modelos.
    """
)


# ============================================================
# ESTÁGIO 1
# ============================================================

st.header("Capta-PTBR — Estágio 1")

st.markdown(
    """
    O primeiro estágio foi construído a partir da aplicação de
    **padrões léxico-sintáticos** sobre o corpus TuPy-E.

    Os padrões recuperaram **781 ocorrências agregadas**,
    correspondentes a **741 sentenças distintas**. Após a análise,
    **633 sentenças** foram consideradas elegíveis por apresentarem
    caracterização ou citação de pessoa/grupo.
    """
)

arquivo_estagio1 = localizar_csv(
    ESTAGIO_1_DIR
)

mostrar_download_csv(
    arquivo_estagio1,
    "Capta-PTBR — Estágio 1",
    "download_estagio1"
)

if arquivo_estagio1:

    with st.expander(
        "Visualizar amostra do Estágio 1"
    ):

        visualizar_csv(
            arquivo_estagio1
        )


# ============================================================
# DIVISOR
# ============================================================

st.divider()


# ============================================================
# ESTÁGIO 2
# ============================================================

st.header("Capta-PTBR — Estágio 2")

st.markdown(
    """
    O segundo estágio corresponde ao conjunto utilizado na
    **anotação manual**, contendo **1.500 sentenças**.

    A anotação resultou em:

    - **588 sentenças capacitistas**
    - **912 sentenças não capacitistas**

    Esse conjunto foi utilizado para ampliar a representação da
    classe capacitista e fornecer exemplos contextualizados para
    os experimentos de treinamento e avaliação.
    """
)

arquivo_estagio2 = localizar_csv(
    ESTAGIO_2_DIR
)

mostrar_download_csv(
    arquivo_estagio2,
    "Capta-PTBR — Estágio 2",
    "download_estagio2"
)

if arquivo_estagio2:

    with st.expander(
        "Visualizar amostra do Estágio 2"
    ):

        visualizar_csv(
            arquivo_estagio2
        )


# ============================================================
# DIVISOR
# ============================================================

st.divider()


# ============================================================
# VALIDAÇÃO DAS PREDIÇÕES
# ============================================================

st.header("Validação das Predições")

st.markdown(
    """
    Após o treinamento, as predições produzidas pelo modelo sobre
    o **BiasTube-PTBR** foram confrontadas com a anotação manual.

    Esse conjunto permite analisar a correspondência entre a
    **classificação humana** e a **predição automática**, além de
    identificar casos de concordância, falsos positivos e falsos
    negativos.

    O arquivo disponibilizado nesta seção preserva os dados
    utilizados nessa etapa de validação.
    """
)


arquivo_validacao = localizar_csv(
    VALIDACAO_DIR
)


# ============================================================
# DOWNLOAD
# ============================================================

mostrar_download_csv(
    arquivo_validacao,
    "Validação das Predições",
    "download_validacao"
)


# ============================================================
# VISUALIZAÇÃO
# ============================================================

if arquivo_validacao:

    df_validacao = carregar_csv(
        arquivo_validacao
    )

    if df_validacao is not None:

        st.caption(
            f"{len(df_validacao):,} registros disponíveis "
            f"para validação."
        )

        with st.expander(
            "Visualizar amostra da validação"
        ):

            st.dataframe(
                df_validacao.head(50),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# FOOTER
# ============================================================

footer()