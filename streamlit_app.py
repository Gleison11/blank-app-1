from pathlib import Path

import streamlit as st
import pandas as pd

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="Consulta de Validade",
    page_icon="📦",
    layout="wide"
)

# ==============================
# TÍTULO
# ==============================

st.title("📦 Consulta de Validade da Carga")
st.write("Informe o número da Guia para verificar a carga.")

# ==============================
# CARREGAR A PLANILHA
# ==============================

arquivo = Path(__file__).parent / "DCP - Estoque em Trânsito_CD x Loja_Tabela (1).csv"

@st.cache_data
def carregar_planilha(caminho_arquivo):
    if not caminho_arquivo.exists():
        st.error(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        st.stop()

    base = pd.read_csv(
        caminho_arquivo,
        sep=";",
        encoding="utf-8-sig",
        dtype={"Guia": str}
    )

    # Limpa nomes das colunas
    base.columns = base.columns.astype(str).str.strip()

    # Padroniza a coluna Guia
    if "Guia" in base.columns:
        base["Guia"] = (
            base["Guia"]
            .astype(str)
            .str.strip()
            .str.replace(".0", "", regex=False)
        )

    return base


base = carregar_planilha(arquivo)

# ==============================
# CAMPO DA GUIA
# ==============================

guia = st.text_input(
    "Número da Guia",
    placeholder="Digite o número da Guia"
)

# ==============================
# BOTÃO CONSULTAR
# ==============================

if st.button("🔎 CONSULTAR", type="primary"):

    numero_guia = str(guia).strip()

    if numero_guia == "":
        st.warning("⚠️ Digite o número da Guia.")

    else:

        # ==============================
        # CONSULTA
        # ==============================

        resultado = base[
            base["Guia"] == numero_guia
        ]

        # ==============================
        # GUIA NÃO ENCONTRADA
        # ==============================

        if resultado.empty:

            st.error("❌ Guia não encontrada.")

            st.info(
                "Verifique se o número da Guia foi digitado corretamente."
            )

        # ==============================
        # GUIA ENCONTRADA
        # ==============================

        else:

            st.error("🔴 ATENÇÃO — CARGA COM ITENS CRÍTICOS")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Número da Guia",
                    numero_guia
                )

            with col2:
                st.metric(
                    "Registros encontrados",
                    len(resultado)
                )

            st.subheader("📋 Itens encontrados")

            st.dataframe(
                resultado,
                use_container_width=True,
                hide_index=True
            )
