import requests
import pandas as pd


# ==========================================
# DIA 2 - IDENTIFICAÇÃO DOS PERÍODOS
# ==========================================


# API do Banco Central
url_periodos = "https://www3.bcb.gov.br/rdrweb/rest/ext/ranking"


# Consulta os períodos disponíveis
resposta_periodos = requests.get(url_periodos)

dados = resposta_periodos.json()

anos = dados["anos"]


# ==========================================
# ORGANIZAR OS PERÍODOS
# ==========================================

periodos = []

for ano in anos:

    for periodicidade in ano["periodicidades"]:

        for periodo in periodicidade["periodos"]:

            for tipo in periodo["tipos"]:

               periodos.append({
                 "ano": ano["ano"],
                "periodicidade": periodicidade["periodicidade"],
                 "periodo": periodo["periodo"],
                 "tipo": tipo["tipo"]
               })


# Criar DataFrame
df_periodos = pd.DataFrame(periodos)

# Converter ano para número
df_periodos["ano"] = pd.to_numeric(
    df_periodos["ano"],
    errors="coerce"
)


# ==========================================
# FILTRAR BANCOS E FINANCEIRAS
# ==========================================

df_bancos = df_periodos[
    df_periodos["tipo"] == "Bancos e financeiras"
]


# ==========================================
# SELECIONAR PERÍODO DO ESTUDO
# ==========================================

df_periodo_estudo = df_bancos[
    df_bancos["ano"] >= 2017
].copy()


# ==========================================
# SALVAR PERÍODOS
# ==========================================

df_periodo_estudo.to_csv(
    "data/raw/periodos_estudo.csv",
    index=False
)


# ==========================================
# CONFERÊNCIA
# ==========================================

print("Arquivo de períodos salvo com sucesso!")

print(
    f"Períodos encontrados: {len(df_periodo_estudo)}"
)

print("\nÚltimos períodos:")

print(
    df_periodo_estudo.tail()
)