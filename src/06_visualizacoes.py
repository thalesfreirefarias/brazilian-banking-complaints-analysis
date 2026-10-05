# ============================================================
# DIA 6 - VISUALIZAÇÕES
# Projeto: Churn Bancário Brasil
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/reclamacoes_historico.csv")

print(df.shape)
print(df.columns)


# ------------------------------------------------------------
# GRÁFICO 1 - EVOLUÇÃO DAS RECLAMAÇÕES PROCEDENTES (2017-2025)
# ------------------------------------------------------------

df_periodo = df[
    (df["ano"] >= 2017) &
    (df["ano"] <= 2025)
]

evolucao_anual = (
    df_periodo
    .groupby("ano")["procedentes"]
    .sum()
)

plt.plot(
    evolucao_anual.index,
    evolucao_anual.values,
    marker="o"
)

plt.title("Evolução das Reclamações Procedentes (2017–2025)")
plt.xlabel("Ano")
plt.ylabel("Reclamações procedentes")
plt.grid(alpha=0.3)

for ano, valor in evolucao_anual.items():
    plt.text(
        ano,
        valor + 4000,
        f"{valor:,.0f}".replace(",", "."),
        ha="center"
    )

    plt.ylim(top=evolucao_anual.max() * 1.12)

plt.tight_layout()

plt.savefig(
    "outputs/grafico_01_evolucao_procedentes.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ------------------------------------------------------------
# GRÁFICO 2 - TOP 10 INSTITUIÇÕES POR RECLAMAÇÕES PROCEDENTES (2025)
# ------------------------------------------------------------

df_2025 = df[df["ano"] == 2025]

top10_2025 = (
    df_2025
    .groupby("instituicao")["procedentes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top10_2025.index = (
    top10_2025.index
    .str.replace(" (conglomerado)", "", regex=False)
)

plt.figure(figsize=(14, 7))

top10_2025.sort_values().plot(
    kind="barh"
)

plt.title(
    "Top 10 Instituições por Reclamações Procedentes em 2025",
    fontsize=16
)

plt.xlabel("Reclamações procedentes")
plt.ylabel("Instituição")

plt.grid(
    axis="x",
    alpha=0.3
)

# Adiciona os valores ao final de cada barra
for i, valor in enumerate(top10_2025.sort_values()):
    plt.text(
        valor + 200,
        i,
        f"{valor:,.0f}".replace(",", "."),
        va="center"
    )

# Cria espaço para os valores à direita
plt.xlim(
    right=top10_2025.max() * 1.12
)

plt.tight_layout()

plt.savefig(
    "outputs/grafico_02_top10_2025.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ------------------------------------------------------------
# GRÁFICO 3 - EVOLUÇÃO DAS PRINCIPAIS INSTITUIÇÕES (2017-2025)
# ------------------------------------------------------------

# Seleciona o período analisado
df_evolucao = df[
    (df["ano"] >= 2017) &
    (df["ano"] <= 2025)
].copy()


# Padroniza os nomes das instituições
def padronizar_instituicao(nome):

    nome = str(nome).upper()

    if "BRADESCO" in nome:
        return "BRADESCO"

    elif "ITAU" in nome:
        return "ITAU"

    elif "CAIXA ECONÔMICA FEDERAL" in nome:
        return "CAIXA"

    elif "AGIBANK" in nome or "AGIPLAN" in nome:
        return "AGIBANK"

    elif "PICPAY" in nome:
        return "PICPAY"

    return None


df_evolucao["instituicao_padronizada"] = (
    df_evolucao["instituicao"]
    .apply(padronizar_instituicao)
)


# Mantém somente as instituições selecionadas
df_evolucao = df_evolucao[
    df_evolucao["instituicao_padronizada"].notna()
]


# Soma as reclamações procedentes por ano e instituição
evolucao_bancos = (
    df_evolucao
    .groupby(
        ["ano", "instituicao_padronizada"]
    )["procedentes"]
    .sum()
    .reset_index()
)


# Criação do gráfico
plt.figure(figsize=(12, 7))

for banco in [
    "BRADESCO",
    "ITAU",
    "CAIXA",
    "AGIBANK",
    "PICPAY"
]:

    dados_banco = evolucao_bancos[
        evolucao_bancos["instituicao_padronizada"] == banco
    ]

    plt.plot(
        dados_banco["ano"],
        dados_banco["procedentes"],
        marker="o",
        label=banco
    )


# Formatação
plt.title(
    "Evolução das Reclamações Procedentes por Instituição (2017–2025)",
    fontsize=16
)

plt.xlabel("Ano")
plt.ylabel("Reclamações procedentes")

plt.legend(title="Instituição")

plt.grid(alpha=0.3)

plt.xticks(range(2017, 2026))

plt.tight_layout()


# Salva o gráfico
plt.savefig(
    "outputs/grafico_03_evolucao_instituicoes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()