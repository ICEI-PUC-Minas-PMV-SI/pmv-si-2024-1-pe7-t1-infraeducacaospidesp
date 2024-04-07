import pandas as pd

# Ler os dados das tabelas
table1 = pd.read_csv("infraestrutura.csv", sep=';')  # csv separado por ';'
table2 = pd.read_csv("notas.csv", sep=';')          # csv separado por ';'

categories = ["BANHEIROS", "COZINHA", "LABORATÓRIO", "ESPORTE", "SALAS DE AULA", "LEITURA", "OUTROS"]

# Criar um novo DataFrame para armazenar os resultados
results = pd.DataFrame()

# Iterar sobre cada COD_ESC
for cod_esc in table1['COD_ESC'].unique():
    # Filtrar a table1 para o COD_ESC atual
    school_data = table1[table1['COD_ESC'] == cod_esc]
    # Inicializar um dicionário para armazenar a contagem de cada categoria
    categories_count = {}
    # Iterar sobre cada categoria
    for category in categories:
        # Somar a quantidade para a categoria atual
        categories_count[category] = school_data[school_data['CATEGORIA'] == category]['QTD'].sum()
    # Adicionar as contagens como uma nova linha no DataFrame de results
    results = pd.concat([results, pd.DataFrame({'COD_ESC': [cod_esc], **categories_count})], ignore_index=True)

# Merge table2 com results baseado em COD_ESC
merged_results = pd.merge(results, table2[['COD_ESC', 'IDESP_AI', 'IDESP_AF', 'IDESP_EM', 'ANO_APLICACAO', 'DTCADASTRO']], on='COD_ESC', how='inner')
merged_results.to_csv("resultados_completos.csv", index=False)

