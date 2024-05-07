import pandas as pd

# Ler os dados das tabelas
table1 = pd.read_csv("infraestrutura.csv", sep=';')  # csv separado por ';'
table2 = pd.read_csv("notas.csv", sep=';')          # csv separado por ';'

print(table1,table2)


# Filtrando e agrupar df_infraestrutura, não separamos os filtros por escola mais porque nos foi pedido para ignorar os dados de código de escola
# e que escola pode constar em mais de uma linha desde que em anos distintos
categories =table1[table1["CATEGORIA"].isin(["BANHEIROS", "COZINHA", "LABORATÓRIO", "ESPORTE", "SALAS DE AULA", "LEITURA", "OUTROS"])]
categories_count = categories.groupby(["COD_ESC", "CATEGORIA"])['QTD'].sum().unstack(fill_value=0)


# Merge table2 com results baseado em COD_ESC
merged_results = pd.merge(table2, categories_count, on='COD_ESC', how='inner')

# Elimina valores nulos como nos foi pedido
merged_results_filtrados = merged_results.dropna(subset=['IDESP_AF'])

# Deixando só os dados que nos pediram, eliminando outras notas, código de escola, dados de datas...
resultados_finais = merged_results_filtrados[['BANHEIROS', 'COZINHA', 'LABORATÓRIO', 'ESPORTE', 'SALAS DE AULA', 'LEITURA', 'OUTROS', 'IDESP_AF']];

# Gera os resultados
resultados_finais.to_csv("resultados_completos.csv", index=False)

