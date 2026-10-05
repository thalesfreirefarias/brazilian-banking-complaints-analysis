import pandas as pd

# =========================
# CARREGAMENTO DOS DADOS
# =========================

df = pd.read_csv("data/raw/reclamacoes_historico.csv")


# =========================
# 1. EVOLUÇÃO DAS RECLAMAÇÕES POR ANO
# =========================
reclamacoes_por_ano = df.groupby("ano")["total_reclamacao"].sum()


print("\n" + "=" * 60)
print("1. EVOLUÇÃO DAS RECLAMAÇÕES POR ANO")
print("=" * 60)
print(reclamacoes_por_ano)

# =========================
# 2. INSTITUIÇÕES COM MAIS RECLAMAÇÕES EM 2025
# =========================

reclamacoes_2025 = df[df["ano"] == 2025]
top_10_2025 = (
    reclamacoes_2025
    .groupby("instituicao")["total_reclamacao"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("2. TOP 10 INSTITUIÇÕES POR RECLAMAÇÕES - 2025")
print("=" * 60)
print(top_10_2025)


# =========================
# 3. INSTITUIÇÕES COM MAIS RECLAMAÇÕES PROCEDENTES
# =========================

reclamacoes_2025 = df[df["ano"] == 2025]

top_10_procedentes_2025 = (
    reclamacoes_2025
    .groupby("instituicao")["procedentes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("3. TOP 10 RECLAMAÇÕES PROCEDENTES - 2025")
print("=" * 60)
print(top_10_procedentes_2025)

# =========================
# 4. EVOLUÇÃO DO NÚMERO DE RECLAMAÇÕES PROCEDENTES AO LONGO DOS ANOS
# =========================

top_5_instituicoes = top_10_procedentes_2025.head(5).index

df_top_5 = df[
    df["instituicao"].isin(top_5_instituicoes)
]

evolucao_top_5 = (
    df_top_5
    .groupby(["ano", "instituicao"])["procedentes"]
    .sum()
)


print("\n" + "=" * 60)
print("4. EVOLUÇÃO DAS RECLAMAÇÕES PROCEDENTES - TOP 5")
print("=" * 60)
print(evolucao_top_5)
# =========================
# 5. RELAÇÃO ENTRE CLIENTES E RECLAMAÇÕES
# =========================
df["total_cliente"] = pd.to_numeric(
    df["total_cliente"],
    errors="coerce"
)

df["reclamacoes_100k_clientes"] = (
    df["total_reclamacao"] / df["total_cliente"]
) * 100000


# Recria o filtro após criar a nova coluna
df_top_5 = df[
    df["instituicao"].isin(top_5_instituicoes)
]


taxa_por_ano = (
    df_top_5
    .groupby(["ano", "instituicao"])["reclamacoes_100k_clientes"]
    .mean()
)


print("\n" + "=" * 60)
print("5. TAXA DE RECLAMAÇÕES POR 100 MIL CLIENTES - TOP 5")
print("=" * 60)
print(taxa_por_ano)
# =========================
# 6. PRINCIPAIS INSIGHTS
# =========================

##Insight 1 — Crescimento recente das reclamações:
##O volume total de reclamações apresentou forte crescimento a partir de 2024, passando de aproximadamente 236 mil em 2023 para 598 mil em 2024 e 1,08 milhão em 2025.

##Insight 2 — Volume absoluto não conta toda a história:
##Bradesco liderou o volume de reclamações procedentes em 2025, com 24.886 registros. Entretanto, ao normalizar o volume de reclamações pelo número de clientes, o Agibank apresentou uma taxa proporcional significativamente superior às demais instituições analisadas.

##Insight 3 — Mudança no comportamento do Agibank:
##O Agibank apresentou crescimento expressivo nos anos mais recentes. As reclamações procedentes passaram de 1.234 em 2023 para 6.492 em 2024 e 13.797 em 2025. Na média trimestral de reclamações por 100 mil clientes, passou de aproximadamente 38,46 em 2023 para 113,26 em 2024 e 120,95 em 2025.

##Insight 4 — Cuidado com 2026:
##Os dados de 2026 representam um período ainda incompleto e, portanto, não devem ser comparados diretamente com os totais anuais dos anos anteriores.