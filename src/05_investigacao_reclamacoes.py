# ============================================================
# DIA 5 - INVESTIGAÇÃO DO AUMENTO DAS RECLAMAÇÕES
# Projeto: Churn Bancário Brasil
# ============================================================


# ------------------------------------------------------------
# 1. PREPARAÇÃO DOS DADOS
# ------------------------------------------------------------

import pandas as pd

df = pd.read_csv("data/raw/reclamacoes_historico.csv")

print(df.columns)


# ------------------------------------------------------------
# 2. EVOLUÇÃO DAS RECLAMAÇÕES
# ------------------------------------------------------------

# Pergunta:
# Como o volume de reclamações evoluiu ao longo dos anos?

reclamacoes_ano = df.groupby("ano")["procedentes"].sum()

print("\nReclamações procedentes por ano:")
print(reclamacoes_ano)


# Pergunta:
# O crescimento observado em 2024 e 2025 realmente foi
# diferente dos anos anteriores?

variacao_anual = reclamacoes_ano.pct_change() * 100

print("\nVariação anual das reclamações procedentes (%):")
print(variacao_anual)


# ACHADO:
# 2024 apresentou a maior variação anual da série: +132,06%.
# 2020 teve a segunda maior alta: +72,15%.
# 2025 manteve a tendência de crescimento: +36,84%.


# ------------------------------------------------------------
# 3. CRESCIMENTO DA BASE DE CLIENTES
# ------------------------------------------------------------

# Pergunta:
# Nos bancos que mais tiveram reclamações, o aumento das reclamações
# foi acompanhado pelo crescimento da base de clientes?

# Bancos selecionados a partir da análise anterior
top_bancos = [
    "AGIBANK (conglomerado)",
    "BRADESCO (conglomerado)",
    "CAIXA ECONÔMICA FEDERAL (conglomerado)",
    "ITAU (conglomerado)",
    "PICPAY (conglomerado)"
]

# Filtra somente os bancos selecionados
df_top = df[
    df["instituicao"].isin(top_bancos)
].copy()


# Garante que total_cliente seja numérico
df_top["total_cliente"] = pd.to_numeric(
    df_top["total_cliente"],
    errors="coerce"
)


# Cria tabela anual por instituição
analise_top = (
    df_top
    .groupby(["ano", "instituicao"])
    .agg(
        procedentes=("procedentes", "sum"),
        clientes_medio=("total_cliente", "mean")
    )
    .reset_index()
)


# Crescimento anual das reclamações de cada instituição
analise_top["crescimento_reclamacoes_%"] = (
    analise_top
    .groupby("instituicao")["procedentes"]
    .pct_change() * 100
)


# Crescimento anual da base média de clientes
analise_top["crescimento_clientes_%"] = (
    analise_top
    .groupby("instituicao")["clientes_medio"]
    .pct_change() * 100
)


# Arredonda os valores
analise_top["clientes_medio"] = (
    analise_top["clientes_medio"].round(2)
)

analise_top["crescimento_reclamacoes_%"] = (
    analise_top["crescimento_reclamacoes_%"].round(2)
)

analise_top["crescimento_clientes_%"] = (
    analise_top["crescimento_clientes_%"].round(2)
)


# Exibe somente 2024 e 2025
print("\nAnálise dos principais bancos - 2024 e 2025:")

print(
    analise_top[
        analise_top["ano"].isin([2024, 2025])
    ]
)


# Pergunta:
# O crescimento das reclamações foi maior ou menor
# que o crescimento da base de clientes?

# ACHADO:
# O crescimento da base de clientes, isoladamente, não parece explicar
# o aumento das reclamações nos principais bancos.
#
# Em 2024, Agibank, Bradesco, Caixa e Itaú apresentaram crescimento
# das reclamações muito superior à variação da base de clientes.
#
# No Itaú, por exemplo, as reclamações aumentaram 117,89%,
# enquanto a base média de clientes apresentou queda de 0,61%.


# ------------------------------------------------------------
# 4. INSTITUIÇÕES QUE EXPLICAM O AUMENTO
# ------------------------------------------------------------

# Pergunta:
# Quais instituições tiveram o maior crescimento
# de reclamações em 2024 e 2025?

# 2024:
# - Agibank: +426,09%
# - Itaú: +117,89%
# - Caixa: +102,48%
# - Bradesco: +21,38%
# - PicPay: sem comparação anterior nesse recorte
#
# 2025:
# - PicPay: +579,58%
# - Agibank: +112,52%
# - Bradesco: +92,01%
# - Itaú: +15,11%
# - Caixa: -0,45%


# Pergunta:
# Quais bancos mais contribuíram para o aumento
# total das reclamações?

analise_top["aumento_reclamacoes"] = (
    analise_top
    .groupby("instituicao")["procedentes"]
    .diff()
)


# Exibe os resultados de 2024 e 2025
print("\nContribuição dos principais bancos para o aumento:")

print(
    analise_top[
        analise_top["ano"].isin([2024, 2025])
    ][
        [
            "ano",
            "instituicao",
            "procedentes",
            "crescimento_reclamacoes_%",
            "aumento_reclamacoes"
        ]
    ]
)


# ACHADO:
# Em 2024, Itaú (+7.275) e Caixa (+7.239) foram as instituições
# que mais adicionaram reclamações procedentes em números absolutos.
#
# Apesar de o Agibank apresentar o maior crescimento percentual
# (+426,09%), seu aumento absoluto foi menor (+5.258).
#
# Em 2025, Bradesco (+11.925) e PicPay (+10.131) apresentaram
# os maiores aumentos absolutos entre as instituições analisadas.
#
# A Caixa apresentou estabilidade, com redução de 64 reclamações.
#
# Portanto, crescimento percentual e contribuição absoluta
# apresentam perspectivas diferentes sobre o aumento das reclamações.


# ------------------------------------------------------------
# 5. RECLAMAÇÕES PROPORCIONAIS À BASE DE CLIENTES
# ------------------------------------------------------------

# Pergunta:
# Considerando o tamanho da base de clientes,
# quais instituições apresentam maior taxa de reclamações?

analise_top["reclamacoes_100k_clientes"] = (
    analise_top["procedentes"]
    / analise_top["clientes_medio"]
    * 100000
)


# Arredonda a taxa para duas casas decimais
analise_top["reclamacoes_100k_clientes"] = (
    analise_top["reclamacoes_100k_clientes"].round(2)
)


print("\nReclamações por 100 mil clientes - 2024 e 2025:")

print(
    analise_top[
        analise_top["ano"].isin([2024, 2025])
    ][
        [
            "ano",
            "instituicao",
            "procedentes",
            "clientes_medio",
            "reclamacoes_100k_clientes"
        ]
    ]
)


# ACHADO:
# Ao considerar o tamanho da base de clientes, o Agibank apresentou
# a maior taxa de reclamações entre as instituições analisadas:
# 203,24 reclamações por 100 mil clientes em 2024 e 248,35 em 2025.
#
# O PicPay também apresentou forte aumento proporcional, passando
# de 2,90 para 18,37 reclamações por 100 mil clientes.
#
# A Caixa permaneceu praticamente estável, passando de 9,28 para 9,08.
#
# Portanto, o aumento observado não pode ser explicado apenas
# pelo tamanho ou crescimento da base de clientes.


# ------------------------------------------------------------
# 6. CONCLUSÃO DA INVESTIGAÇÃO
# ------------------------------------------------------------

# CONCLUSÃO:
# A análise identificou um forte crescimento das reclamações
# procedentes em 2024, com continuidade do aumento em 2025.
#
# O crescimento da base de clientes não foi suficiente para explicar
# esse movimento. Em diversas instituições, as reclamações cresceram
# muito acima da variação da quantidade de clientes.
#
# Em 2024, Itaú e Caixa apresentaram os maiores aumentos absolutos
# de reclamações entre as instituições analisadas.
#
# Em 2025, Bradesco e PicPay apresentaram os maiores
# aumentos absolutos.
#
# Quando as reclamações foram normalizadas pela base de clientes,
# o Agibank apresentou a maior taxa entre as instituições analisadas.
#
# LIMITAÇÃO:
# A base utilizada não contém o motivo detalhado das reclamações.
# Portanto, não é possível determinar apenas com estes dados se
# o crescimento está relacionado a atendimento, produtos, fraudes,
# cobranças, canais digitais ou outros fatores.
#
# Uma versão futura do projeto poderá incorporar dados detalhados
# sobre os motivos das reclamações para aprofundar a investigação.