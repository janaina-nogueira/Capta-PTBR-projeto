from pathlib import Path

import streamlit as st

from site_utils import apply_theme, header_logos, footer


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Análises | Capta-PTBR",
    page_icon="📊",
    layout="wide"
)

apply_theme()
header_logos()


# ============================================================
# CAMINHOS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
ANALISES_DIR = ROOT / "analises"


# ============================================================
# FUNÇÕES
# ============================================================

def tamanho_legivel(numero_bytes):
    tamanho = float(numero_bytes)

    for unidade in ["B", "KB", "MB", "GB"]:
        if tamanho < 1024:
            return f"{tamanho:.1f} {unidade}"

        tamanho /= 1024

    return f"{tamanho:.1f} TB"


def mime_arquivo(arquivo: Path):

    extensao = arquivo.suffix.lower()

    tipos = {
        ".py": "text/x-python",
        ".ipynb": "application/json",
        ".csv": "text/csv",
        ".json": "application/json",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".html": "text/html",
        ".zip": "application/zip",
        ".pdf": "application/pdf",
    }

    return tipos.get(
        extensao,
        "application/octet-stream"
    )


def botao_download(arquivo: Path, chave: str):

    try:
        dados = arquivo.read_bytes()

        st.download_button(
            label="⬇ Baixar",
            data=dados,
            file_name=arquivo.name,
            mime=mime_arquivo(arquivo),
            key=chave,
            on_click="ignore"
        )

    except Exception as erro:
        st.error(
            f"Erro ao ler {arquivo.name}: {erro}"
        )


# ============================================================
# PÁGINA
# ============================================================

st.title("Análises")

st.markdown(
    """
    Esta seção reúne os **códigos, notebooks e arquivos utilizados
    nas análises computacionais do Capta-PTBR**.

    Os arquivos podem ser baixados diretamente pelo website.
    """
)


# ============================================================
# VERIFICAÇÃO
# ============================================================

if not ANALISES_DIR.exists():

    st.error(
        f"Pasta não encontrada:\n\n`{ANALISES_DIR}`"
    )

    st.stop()


# ============================================================
# TODOS OS ARQUIVOS
# ============================================================

arquivos = sorted(
    [
        arquivo
        for arquivo in ANALISES_DIR.rglob("*")
        if arquivo.is_file()
    ],
    key=lambda x: str(x).lower()
)


if not arquivos:

    st.info(
        "Nenhum arquivo foi encontrado na pasta de análises."
    )

else:

    st.caption(
        f"{len(arquivos)} arquivo(s) disponível(is)."
    )

    st.divider()

    for indice, arquivo in enumerate(arquivos):

        relativo = arquivo.relative_to(
            ANALISES_DIR
        )

        col_nome, col_download = st.columns(
            [5, 1]
        )

        with col_nome:

            st.markdown(
                f"**{arquivo.name}**"
            )

            st.caption(
                f"{relativo} · "
                f"{tamanho_legivel(arquivo.stat().st_size)}"
            )

        with col_download:

            botao_download(
                arquivo,
                f"download_analise_{indice}"
            )


footer()