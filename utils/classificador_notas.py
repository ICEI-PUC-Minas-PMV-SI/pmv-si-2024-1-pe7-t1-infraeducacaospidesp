import pandas as pd

# Categorias para classificar as notas
categorias_classificacao_notas = ["E", "D", "C", "B", "A"]

# Função que recebe a nota e o intervalo que deve ser utilizado para classificar as notas
# dentro das categorias e classifica em qual categoria a nota esta
def classificar_nota(nota, intervalo_classificacao):
    for index, item in enumerate(categorias_classificacao_notas):
        if nota <= ((index + 1) * intervalo_classificacao):
            return item
    return categorias_classificacao_notas[0]

# Calcula com base na nota minima, na nota máxima e na quantidade de categorias
# o intervalo que deve ser utilizado para realizar a classificação das notas nas categorias
def calcular_intervalo_classificacao(dados):
    min = dados["IDESP_AF"].min()
    max = dados["IDESP_AF"].max()
    quantidade_categorias = len(categorias_classificacao_notas)
    return (min + max) / quantidade_categorias

# Função para realizar o processamento das notas e classificar elas nas categorias correspondentes
def processar(dados):
    intervalo_categorizacao = calcular_intervalo_classificacao(dados)
    dados["CLASSIFICACAO_NOTA"] = dados["IDESP_AF"].map((lambda x: classificar_nota(x, intervalo_categorizacao)))
    return dados

## Inicio da execução ##
# Leitura dos dados
dados = pd.read_csv("resultados_completos.csv", sep=',')
dados_processados = processar(dados)

# Gera os resultados em um arquivo CSV
dados_processados.to_csv("resultados_completos_classificados.csv", index=False)


