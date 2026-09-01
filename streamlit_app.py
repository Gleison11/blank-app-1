from pathlib import Path

import pandas as pd
import streamlit as st

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="Consulta de Validade",
    page_icon="📦",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
        }
        .main {
            background: transparent;
        }
        .card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 1.5rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        }
        .label {
            font-size: 1.1rem;
            font-weight: 600;
            color: #0f172a;
        }
        .subtext {
            color: #475569;
            font-size: 0.98rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================
# TÍTULO
# ==============================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("📦 Consulta de Validade da Carga")
st.caption("Consulte os registros por uma loja específica.")

# ==============================
# CARREGAR A PLANILHA
# ==============================

arquivo = Path(__file__).parent / "Atualização1.csv"


@st.cache_data
def carregar_planilha(caminho_arquivo):
    if not caminho_arquivo.exists():
        st.error(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        st.stop()

    base = pd.read_csv(
        caminho_arquivo,
        sep=";",
        encoding="utf-8-sig",
        dtype={"Guia": str, "Loja": str},
    )

    base.columns = base.columns.astype(str).str.strip()

    for coluna in ["Guia", "Loja"]:
        if coluna in base.columns:
            base[coluna] = (
                base[coluna]
                .astype(str)
                .str.strip()
                .str.replace(".0", "", regex=False)
            )

    return base


base = carregar_planilha(arquivo)

# ==============================
# FORMULÁRIO DE CONSULTA
# ==============================

with st.form("consulta_loja"):
    loja = st.text_input(
        "Número da Loja",
        placeholder="Digite o número da loja",
        max_chars=20,
    )
    enviado = st.form_submit_button("🔎 CONSULTAR", use_container_width=True)

if enviado:
    numero_loja = loja.strip()

    if not numero_loja:
        st.warning("⚠️ Digite o número da loja antes de consultar.")
    else:
        resultado = base[base["Loja"].astype(str).str.strip().eq(numero_loja)]

        if resultado.empty:
            st.error("❌ Nenhuma loja encontrada.")
            st.info("Verifique se o número da loja foi digitado corretamente.")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.error("🔴 ATENÇÃO — CARGA COM ITENS CRÍTICOS")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Loja consultada", numero_loja)
            with col2:
                st.metric("Guias encontradas", resultado["Guia"].nunique())
            with col3:
                st.metric("Registros encontrados", len(resultado))

            st.subheader("📋 Itens encontrados")
            st.dataframe(
                resultado[["Loja", "Guia", "Data Guia", "Material", "Descricao", "Quantidade", "Montante"]],
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
