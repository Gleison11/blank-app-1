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
st.write("Informe até 5 números de Guia para verificar a carga.")

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
# CAMPOS DAS GUIAS
# ==============================

colunas_guias = st.columns(5)
guias = []

for indice, coluna in enumerate(colunas_guias, start=1):
    with coluna:
        guias.append(
            st.text_input(
                f"Guia {indice}",
                placeholder="Número da Guia",
                key=f"guia_{indice}"
            )
        )

# ==============================
# BOTÃO CONSULTAR
# ==============================

if st.button("🔎 CONSULTAR", type="primary"):

    numeros_guias = [str(numero).strip() for numero in guias if str(numero).strip()]

    if not numeros_guias:
        st.warning("⚠️ Digite pelo menos um número de Guia.")

    else:

        # ==============================
        # CONSULTA
        # ==============================

        resultado = base[base["Guia"].isin(numeros_guias)]
        guias_nao_encontradas = [
            numero for numero in numeros_guias
            if numero not in set(resultado["Guia"])
        ]

        # ==============================
        # GUIA NÃO ENCONTRADA
        # ==============================

        if resultado.empty:

            st.error("❌ Nenhuma guia encontrada.")

            st.info(
                "Verifique se os números das Guias foram digitados corretamente."
            )

        # ==============================
        # GUIAS ENCONTRADAS
        # ==============================

        else:

            st.error("🔴 ATENÇÃO — CARGA COM ITENS CRÍTICOS")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Guias encontradas",
                    resultado["Guia"].nunique()
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

            if guias_nao_encontradas:
                st.warning(
                    "Guias não encontradas: "
                    + ", ".join(guias_nao_encontradas)
                )
