import requests
import pandas as pd
from io import StringIO


# API do Banco Central
url_periodos = "https://www3.bcb.gov.br/rdrweb/rest/ext/ranking"

# Consulta os períodos disponíveis
resposta_periodos = requests.get(url_periodos)
dados = resposta_periodos.json()

anos = dados["anos"]

# Organiza os períodos em uma lista
periodos = []

for ano in anos:
    for periodicidade in ano["periodicidades"]:
        for periodo in periodicidade["periodos"]:
            for tipo in periodo["tipos"]:
                periodos.append({
                    "ano": ano["ano"],
                    "periodicidade": periodicidade["periodicidade"],
                    "periodo": periodo["periodo"],
                    "tipo": tipo
                })

df_periodos = pd.DataFrame(periodos)


# Seleciona bancos e financeiras a partir de 2017
df_bancos = df_periodos[
    df_periodos["tipo"] == "Bancos e financeiras"
]

df_periodo_estudo = df_bancos[
    df_bancos["ano"] >= 2017
]


# Endpoint dos arquivos de reclamações
url_arquivo = "https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo"

resultados = []

# Baixa cada trimestre disponível
for _, linha in df_periodo_estudo.iterrows():

    ano = linha["ano"]
    trimestre = linha["periodo"]

    print(f"Baixando {ano} - {trimestre}º trimestre")

    parametros = {
        "ano": ano,
        "periodicidade": "TRIMESTRAL",
        "periodo": trimestre,
        "tipo": "Bancos e financeiras"
    }

    resposta = requests.get(
        url_arquivo,
        params=parametros
    )

    df_trimestre = pd.read_csv(
        StringIO(resposta.text),
        sep=";"
    )

    resultados.append(df_trimestre)


# Junta todos os períodos
df_reclamacoes = pd.concat(
    resultados,
    ignore_index=True
)


# Remove colunas vazias criadas pelo CSV
df_reclamacoes = df_reclamacoes.loc[
    :,
    ~df_reclamacoes.columns.str.startswith("Unnamed")
]


# Salva a base bruta consolidada
df_reclamacoes.to_csv(
    "data/raw/reclamacoes_bcb_2017_2026.csv",
    index=False
)


# Conferência final
print("\nColeta concluída!")
print(f"Períodos coletados: {len(resultados)}")
print(f"Linhas: {df_reclamacoes.shape[0]}")
print(f"Colunas: {df_reclamacoes.shape[1]}")


df_periodo_estudo.tail(5)