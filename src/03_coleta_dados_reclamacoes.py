import requests
import pandas as pd
from io import BytesIO


# ==========================================
# DIA 3 - COLETA HISTÓRICA DE RECLAMAÇÕES
# ==========================================


# ==========================================
# 1. CARREGAR OS PERÍODOS DO DIA 2
# ==========================================

df_periodo_estudo = pd.read_csv(
    "data/raw/periodos_estudo.csv"
)

print(
    f"Períodos encontrados: {len(df_periodo_estudo)}"
)


# ==========================================
# 2. URL DOS ARQUIVOS DO BANCO CENTRAL
# ==========================================

url_arquivo = (
    "https://www3.bcb.gov.br/"
    "rdrweb/rest/ext/ranking/arquivo"
)


# ==========================================
# 3. LISTA PARA ARMAZENAR OS PERÍODOS
# ==========================================

bases = []


# ==========================================
# 4. PERCORRER TODOS OS PERÍODOS
# ==========================================

for _, linha in df_periodo_estudo.iterrows():

    ano = int(linha["ano"])
    periodicidade = linha["periodicidade"]
    periodo = int(linha["periodo"])
    tipo = linha["tipo"]

    params = {
        "ano": ano,
        "periodicidade": periodicidade,
        "periodo": periodo,
        "tipo": tipo
    }

    print(
        f"Baixando: {ano} | "
        f"{periodicidade} | período {periodo}"
    )


    # ==========================================
    # 5. DOWNLOAD
    # ==========================================

    try:

        response = requests.get(
            url_arquivo,
            params=params,
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException as erro:

        print(
            f"Erro no download: {erro}"
        )

        continue


    # ==========================================
    # 6. LER CSV
    # ==========================================

    try:

        df = pd.read_csv(
            BytesIO(response.content),
            encoding="latin-1",
            sep=";"
        )

    except Exception as erro:

        print(
            f"Erro ao ler arquivo: {erro}"
        )

        continue


    # ==========================================
    # 7. REMOVER COLUNAS UNNAMED
    # ==========================================

    df = df.loc[
        :,
        ~df.columns.str.startswith("Unnamed")
    ]


    # ==========================================
    # 8. COLUNAS BÁSICAS
    # ==========================================

    coluna_instituicao = (
        "Instituição financeira"
    )

    coluna_clientes = (
        "Quantidade total de clientes "
        "\x96 CCS e SCR"
    )


    # ==========================================
    # 9. ESTRUTURA ANTIGA
    # ==========================================

    procedentes_antiga = (
        "Quantidade de reclamações "
        "reguladas procedentes"
    )

    total_antiga = (
        "Quantidade total de reclamações"
    )


    # ==========================================
    # 10. ESTRUTURA NOVA 1 - 2024 T2
    # ==========================================

    procedentes_nova_1 = (
        "Quantidade de reclamações reguladas "
        "procedentes extrapoladas"
    )

    total_nova_1 = (
        "Quantidade total de reclamações "
        "respondidas"
    )


    # ==========================================
    # 11. ESTRUTURA NOVA 2 - 2024 T3+
    # ==========================================

    procedentes_nova_2 = (
        "Quantidade de reclamações "
        "procedentes extrapoladas"
    )

    total_nova_2 = (
        "Quantidade total de reclamações "
        "respondidas"
    )


    # ==========================================
    # 12. IDENTIFICAR ESTRUTURA
    # ==========================================

    if (
        procedentes_antiga in df.columns
        and total_antiga in df.columns
    ):

        coluna_procedentes = (
            procedentes_antiga
        )

        coluna_total = (
            total_antiga
        )

        estrutura = "antiga"


    elif (
        procedentes_nova_1 in df.columns
        and total_nova_1 in df.columns
    ):

        coluna_procedentes = (
            procedentes_nova_1
        )

        coluna_total = (
            total_nova_1
        )

        estrutura = "nova_1"


    elif (
        procedentes_nova_2 in df.columns
        and total_nova_2 in df.columns
    ):

        coluna_procedentes = (
            procedentes_nova_2
        )

        coluna_total = (
            total_nova_2
        )

        estrutura = "nova_2"


    else:

        print(
            "Estrutura não reconhecida. "
            "Pulando período."
        )

        continue


    # ==========================================
    # 13. VERIFICAR COLUNAS BÁSICAS
    # ==========================================

    colunas_basicas = [
        "Ano",
        "Trimestre",
        coluna_instituicao,
        coluna_clientes
    ]

    if not all(
        coluna in df.columns
        for coluna in colunas_basicas
    ):

        print(
            "Colunas básicas ausentes. "
            "Pulando período."
        )

        continue


    # ==========================================
    # 14. SELECIONAR DADOS
    # ==========================================

    df_analise = df[
        [
            "Ano",
            "Trimestre",
            coluna_instituicao,
            coluna_procedentes,
            coluna_total,
            coluna_clientes
        ]
    ].copy()


    # ==========================================
    # 15. PADRONIZAR NOMES
    # ==========================================

    df_analise.columns = [
        "ano",
        "trimestre",
        "instituicao",
        "procedentes",
        "total_reclamacao",
        "total_cliente"
    ]


    # ==========================================
    # 16. REGISTRAR ESTRUTURA
    # ==========================================

    df_analise["estrutura"] = estrutura


    # ==========================================
    # 17. GUARDAR BASE
    # ==========================================

    bases.append(
        df_analise
    )


# ==========================================
# 18. CONSOLIDAR BASE
# ==========================================

if bases:

    df_historico = pd.concat(
        bases,
        ignore_index=True
    )


    # ==========================================
    # 19. SALVAR CSV
    # ==========================================

    df_historico.to_csv(
        "data/raw/reclamacoes_historico.csv",
        index=False
    )


    # ==========================================
    # 20. CONFERÊNCIA
    # ==========================================

    print(
        "\nColeta concluída!"
    )

    print(
        f"Linhas coletadas: "
        f"{len(df_historico)}"
    )


    # ------------------------------------------
    # Anos encontrados
    # ------------------------------------------

    print(
        "\nAnos encontrados:"
    )

    print(
        sorted(
            df_historico[
                "ano"
            ]
            .dropna()
            .unique()
        )
    )


    # ------------------------------------------
    # Estruturas
    # ------------------------------------------

    print(
        "\nEstruturas encontradas:"
    )

    print(
        df_historico[
            "estrutura"
        ]
        .value_counts()
    )


    # ------------------------------------------
    # Registros por ano
    # ------------------------------------------

    print(
        "\nRegistros por ano:"
    )

    print(
        df_historico[
            "ano"
        ]
        .value_counts()
        .sort_index()
    )


    # ------------------------------------------
    # Períodos e estruturas
    # ------------------------------------------

    print(
        "\nPeríodos e estruturas:"
    )

    print(
        df_historico[
            [
                "ano",
                "trimestre",
                "estrutura"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "ano",
                "trimestre"
            ]
        )
        .tail(15)
    )


    # ------------------------------------------
    # Primeiras linhas
    # ------------------------------------------

    print(
        "\nPrimeiras linhas:"
    )

    print(
        df_historico.head()
    )


# ==========================================
# CASO NENHUMA BASE SEJA COLETADA
# ==========================================

else:

    print(
        "\nNenhum período foi coletado."
    )