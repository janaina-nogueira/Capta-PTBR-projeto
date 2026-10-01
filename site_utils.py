
import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == "pages" else Path(__file__).resolve().parent
ASSETS = ROOT / "assets"


def apply_theme():
    st.markdown("""
    <style>

    /* =====================================================
       PALETA CAPTA-PTBR
       ===================================================== */

    :root {
        --cream: #FBF7F1;
        --ink: #16131A;
        --coral: #F58D6B;
        --rose: #E98D9D;
        --lilac: #B9A0C8;
        --muted: #6E6872;
        --line: #E7DDD5;
        --card: #FFFDFC;
    }


    /* =====================================================
       FUNDO
       ===================================================== */

    .stApp {
        background: var(--cream);
        color: var(--ink);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background: #F6EFE8;
        border-right: 1px solid var(--line);
    }


    /* =====================================================
       TÍTULOS
       ===================================================== */

    h1,
    h2,
    h3 {
        color: var(--ink);
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: 3.1rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }


    /* =====================================================
       LINKS
       ===================================================== */

    a {
        color: #8D526F !important;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        padding: 2.4rem 2.6rem;
        border-radius: 28px;

        background:
            radial-gradient(
                circle at 38% 38%,
                rgba(245, 141, 107, .58),
                transparent 26%
            ),
            radial-gradient(
                circle at 68% 42%,
                rgba(185, 160, 200, .55),
                transparent 29%
            ),
            radial-gradient(
                circle at 50% 78%,
                rgba(240, 184, 126, .38),
                transparent 24%
            ),
            #FBF7F1;

        border: 1px solid rgba(231, 221, 213, .8);
        margin-bottom: 1.4rem;
    }


    .eyebrow {
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: #786B73;
    }


    .hero-title {
        font-size: 4rem;
        line-height: 1.03;
        font-weight: 850;
        margin: .5rem 0 1rem;
    }


    .hero-sub {
        font-size: 1.2rem;
        line-height: 1.55;
        max-width: 850px;
    }


    /* =====================================================
       COLUNAS STREAMLIT
       ===================================================== */

    /*
       O maior card da linha define automaticamente
       a altura da linha.
    */

    div[data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }


    /*
       Cada coluna também ocupa toda a altura da linha.
    */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"] {

        display: flex !important;
        flex-direction: column !important;

        min-width: 0 !important;
    }


    /*
       Faz os containers internos do Streamlit
       acompanharem a altura da coluna.
    */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="stColumn"]
    > div[data-testid="stVerticalBlock"] {

        flex: 1 1 auto !important;

        display: flex !important;
        flex-direction: column !important;
    }


    /*
       O elemento que contém o st.markdown
       também precisa crescer.
    */

    div[data-testid="stColumn"]
    div[data-testid="stElementContainer"]:has(.card) {

        flex: 1 1 auto !important;

        display: flex !important;
        flex-direction: column !important;
    }


    div[data-testid="stColumn"]
    div[data-testid="stElementContainer"]:has(.card)
    > div {

        flex: 1 1 auto !important;

        display: flex !important;
        flex-direction: column !important;
    }


    div[data-testid="stColumn"]
    div[data-testid="stElementContainer"]:has(.card)
    div[data-testid="stMarkdownContainer"] {

        flex: 1 1 auto !important;

        display: flex !important;
        flex-direction: column !important;
    }


    /* =====================================================
       CARDS
       ===================================================== */

    /*
       SEM altura fixa.

       O maior conteúdo da linha determina a altura.
       Os outros cards simplesmente acompanham.
    */

    .card {
        background: rgba(255, 253, 252, .78);

        border: 1px solid var(--line);

        border-radius: 18px;

        padding: 1.25rem 1.35rem;

        box-sizing: border-box;

        width: 100%;

        flex: 1 1 auto;

        margin: 0 !important;
    }


    /*
       Remove qualquer altura fixa das classes
       que usamos anteriormente.
    */

    .corpus-card,
    .explore-card {

        height: auto !important;

        min-height: 0 !important;
    }


    /* =====================================================
       ELEMENTOS DOS CARDS
       ===================================================== */

    .card-kicker {
        font-size: .76rem;
        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: .08em;

        color: #9B6578;
    }


    .big {
        font-size: 2.2rem;
        font-weight: 800;

        margin: .1rem 0;
    }


    .muted {
        color: var(--muted);
    }


    /* =====================================================
       PILLS
       ===================================================== */

    .pill {
        display: inline-block;

        padding: .3rem .65rem;

        border-radius: 999px;

        background: #F4E4DF;

        margin: .15rem .25rem .15rem 0;

        font-size: .85rem;
    }


    /* =====================================================
       MÉTRICAS
       ===================================================== */

    /*
       Também sem altura fixa.
       A linha inteira acompanha a maior métrica.
    */

    div[data-testid="stMetric"] {

        background: rgba(255, 253, 252, .8);

        border: 1px solid var(--line);

        padding: 1rem;

        border-radius: 16px;

        box-sizing: border-box;

        width: 100%;

        height: 100%;
    }


    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }


    div[data-testid="stMetricLabel"] {
        font-size: .9rem;
    }


    /* =====================================================
       BOTÕES
       ===================================================== */

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a {

        border-radius: 12px !important;

        border: 1px solid var(--line) !important;

        background: #FFFDFC !important;

        color: var(--ink) !important;

        transition: all .2s ease;
    }


    .stButton > button:hover,
    .stDownloadButton > button:hover {

        border-color: var(--rose) !important;

        background: #F9ECE9 !important;
    }


    /* =====================================================
       DATAFRAMES
       ===================================================== */

    [data-testid="stDataFrame"] {

        border-radius: 14px;

        overflow: hidden;

        border: 1px solid var(--line);
    }


    /* =====================================================
       DIVISORES
       ===================================================== */

    hr {
        border-color: var(--line) !important;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {

        margin-top: 3rem;

        padding-top: 1rem;

        border-top: 1px solid var(--line);

        color: var(--muted);

        font-size: .86rem;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 1.7rem;
            border-radius: 20px;
        }

        .hero-title {
            font-size: 2.8rem;
        }

        .hero-sub {
            font-size: 1rem;
        }

        .card {
            height: auto !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)
    

def header_logos():
    st.markdown("""
    <style>
    .logos-header {
        display: flex;
        align-items: center;
        gap: 28px;
        padding: 8px 0 22px 0;
    }

    .logos-header img {
        height: 75px;
        width: auto;
        object-fit: contain;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    facom = ASSETS / "facom_logo.png"
    ufms = ASSETS / "ufms_logo.png"

    import base64

    def img_base64(path):
        return base64.b64encode(path.read_bytes()).decode()

    if facom.exists() and ufms.exists():

        facom64 = img_base64(facom)
        ufms64 = img_base64(ufms)

        st.markdown(
            f"""
            <div class="logos-header">
                <img src="data:image/png;base64,{facom64}">
                <img src="data:image/png;base64,{ufms64}">
            </div>
            """,
            unsafe_allow_html=True
        )
     

def footer():
    st.markdown('<div class="footer">Capta-PTBR · UFMS · FACOM · PPGCC · Versão 1.0</div>', unsafe_allow_html=True)
