from pathlib import Path
import json
import zipfile

import streamlit as st

from site_utils import apply_theme, header_logos, footer


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Modelos | Capta-PTBR",
    page_icon="🤖",
    layout="wide"
)

apply_theme()
header_logos()


# ============================================================
# CAMINHOS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = ROOT / "models"
DOWNLOADS_DIR = ROOT / "downloads"

DOWNLOADS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# MODELOS DO CAPTA-PTBR
# ============================================================

MODELOS = [
    {
        "pasta": "bertimbau_capta",
        "nome": "BERTimbau + Capta-PTBR",
        "descricao": (
            "Modelo BERTimbau treinado com os recursos "
            "produzidos no Capta-PTBR."
        ),
        "dapt": "Não"
    },

    {
        "pasta": "bertimbau_sem_dapt",
        "nome": "BERTimbau — sem DAPT",
        "descricao": (
            "Modelo BERTimbau utilizado nos experimentos "
            "sem adaptação de domínio."
        ),
        "dapt": "Não"
    },

    {
        "pasta": "berttube_dapt",
        "nome": "BERTtube — com DAPT",
        "descricao": (
            "Modelo resultante da adaptação de domínio "
            "realizada durante os experimentos."
        ),
        "dapt": "Sim"
    }
]


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def tamanho_legivel(numero_bytes):
    """
    Converte bytes para KB, MB, GB etc.
    """

    tamanho = float(numero_bytes)

    for unidade in ["B", "KB", "MB", "GB", "TB"]:

        if tamanho < 1024:
            return f"{tamanho:.1f} {unidade}"

        tamanho /= 1024

    return f"{tamanho:.1f} PB"


def listar_arquivos(pasta):
    """
    Lista todos os arquivos existentes dentro da pasta do modelo.
    """

    if not pasta.exists():
        return []

    return sorted(
        [
            arquivo
            for arquivo in pasta.rglob("*")
            if arquivo.is_file()
        ]
    )


def carregar_config(pasta):
    """
    Lê config.json, caso exista.
    """

    config_path = pasta / "config.json"

    if not config_path.exists():
        return None

    try:

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except Exception:
        return None


def zip_precisa_atualizar(pasta, zip_path):
    """
    Verifica se o ZIP precisa ser criado novamente.
    """

    if not zip_path.exists():
        return True

    data_zip = zip_path.stat().st_mtime

    for arquivo in pasta.rglob("*"):

        if (
            arquivo.is_file()
            and arquivo.stat().st_mtime > data_zip
        ):
            return True

    return False


def criar_zip_modelo(pasta):
    """
    Cria o ZIP do modelo diretamente no disco.

    O arquivo é salvo em:
    downloads/nome_do_modelo.zip
    """

    zip_path = DOWNLOADS_DIR / f"{pasta.name}.zip"

    if not zip_precisa_atualizar(
        pasta,
        zip_path
    ):
        return zip_path

    with zipfile.ZipFile(
        zip_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=6
    ) as zipf:

        for arquivo in pasta.rglob("*"):

            if arquivo.is_file():

                caminho_no_zip = (
                    Path(pasta.name)
                    / arquivo.relative_to(pasta)
                )

                zipf.write(
                    arquivo,
                    arcname=caminho_no_zip
                )

    return zip_path


# ============================================================
# APRESENTAÇÃO DE UM MODELO
# ============================================================

def mostrar_modelo(modelo):

    pasta = MODELS_DIR / modelo["pasta"]

    st.subheader(modelo["nome"])

    st.write(
        modelo["descricao"]
    )

    if not pasta.exists():

        st.warning(
            f"A pasta `models/{modelo['pasta']}` "
            "não foi encontrada."
        )

        return

    arquivos = listar_arquivos(pasta)

    if not arquivos:

        st.info(
            "A pasta deste modelo existe, "
            "mas ainda não possui arquivos."
        )

        return


    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    tamanho_total = sum(
        arquivo.stat().st_size
        for arquivo in arquivos
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Arquivos",
        len(arquivos)
    )

    c2.metric(
        "Tamanho",
        tamanho_legivel(tamanho_total)
    )

    c3.metric(
        "DAPT",
        modelo["dapt"]
    )


    # --------------------------------------------------------
    # ARQUIVOS
    # --------------------------------------------------------

    with st.expander(
        "Arquivos incluídos no modelo"
    ):

        for arquivo in arquivos:

            caminho_relativo = arquivo.relative_to(
                pasta
            )

            tamanho = tamanho_legivel(
                arquivo.stat().st_size
            )

            st.code(
                f"{caminho_relativo}  —  {tamanho}"
            )


    # --------------------------------------------------------
    # CONFIG.JSON
    # --------------------------------------------------------

    config = carregar_config(pasta)

    if config:

        with st.expander(
            "Configuração do modelo"
        ):

            campos_interesse = [
                "architectures",
                "model_type",
                "num_labels",
                "hidden_size",
                "num_hidden_layers",
                "num_attention_heads",
                "vocab_size"
            ]

            dados = {}

            for campo in campos_interesse:

                if campo in config:
                    dados[campo] = config[campo]

            if dados:
                st.json(dados)
            else:
                st.json(config)


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.markdown("#### Download")

    try:

        with st.spinner(
            "Preparando arquivo do modelo..."
        ):

            zip_path = criar_zip_modelo(
                pasta
            )

        tamanho_zip = tamanho_legivel(
            zip_path.stat().st_size
        )

        st.caption(
            f"`{zip_path.name}` • {tamanho_zip}"
        )

        # IMPORTANTE:
        # lê o arquivo antes de criar o botão.
        # O arquivo não fica fechado antes do clique.

        zip_bytes = zip_path.read_bytes()

        st.download_button(
            label="⬇ Baixar modelo completo",
            data=zip_bytes,
            file_name=zip_path.name,
            mime="application/zip",
            key=f"download_modelo_{modelo['pasta']}"
        )

    except Exception as erro:

        st.error(
            "Não foi possível preparar o modelo "
            f"para download.\n\n{erro}"
        )


# ============================================================
# CONTEÚDO DA PÁGINA
# ============================================================

st.title("Modelos")

st.markdown(
    """
    Esta seção reúne os **modelos produzidos e utilizados nos
    experimentos do Capta-PTBR**.

    Os pesos, configurações e arquivos associados são preservados
    dentro do próprio projeto e podem ser obtidos diretamente
    por esta página.
    """
)


# ============================================================
# EXIBIR MODELOS
# ============================================================

for indice, modelo in enumerate(MODELOS):

    mostrar_modelo(modelo)

    if indice < len(MODELOS) - 1:
        st.divider()


footer()